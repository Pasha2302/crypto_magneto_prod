import random
from decimal import Decimal, getcontext, ROUND_HALF_UP
from typing import Dict

from app.db_models import Coin
from app.tasks_all.create_fake_data_coin.tools.base_creator import BaseFakeCreator
from app.tasks_all.create_fake_data_coin.tools.config import PriceFakeConfig, LaunchPriceConfig

getcontext().prec = 28  # достаточная точность для денежных операций


class PriceFakeCreator(BaseFakeCreator):
    """
    Генератор: создает/обновляет поля:
      - price (Decimal, quantize to 1e-18)
      - price_change_24h (float, max 4 dp)
      - high_24h_price (Decimal)
      - low_24h_price (Decimal)
      - launch_price (Decimal, quantize to 1e-8)  <-- добавлено корректно по контракту
    Возвращает dict[field_name -> value] без .save()
    """
    PRICE_QUANT = Decimal("1e-18")
    LAUNCH_PRICE_QUANT = Decimal("1e-8")

    def __init__(self, price_config: PriceFakeConfig = None, launch_config: LaunchPriceConfig = None):
        self.config = price_config or PriceFakeConfig()
        self.launch_config = launch_config or LaunchPriceConfig()

        if self.config.random_seed is not None:
            self._rand = random.Random(self.config.random_seed)
        else:
            self._rand = random.Random()

    @staticmethod
    def _decimal(value) -> Decimal:
        # helper: возвращает Decimal из float/int/Decimal/str
        return Decimal(str(value))

    def _initial_price(self) -> Decimal:
        """Генерируем начальную цену согласно стратегии"""
        mn = self.config.initial_min
        mx = self.config.initial_max
        strat = self.config.initial_strategy

        if strat == "uniform":
            return self._decimal(self._rand.uniform(mn, mx))
        elif strat == "loguniform":
            # log-uniform: полезно для распред. цен по порядкам
            import math
            log_min = math.log(max(mn, 1e-18))
            log_max = math.log(max(mx, mn * 10))
            v = math.exp(self._rand.uniform(log_min, log_max))
            return self._decimal(v)
        elif strat == "based_on_market_cap":
            # можно расширить: если у монеты есть market_cap — вычисляем старт
            # но этот метод не знает coin — поэтому в generate() используем реализацию
            return self._decimal(self._rand.uniform(mn, mx))
        else:
            raise ValueError("Unsupported initial strategy: " + str(strat))

    def _percent_change(self, price: Decimal) -> float:
        """Вычисляем процент изменения, configurable"""
        lo = self.config.volatility_min_percent
        hi = self.config.volatility_max_percent

        if self.config.scale_volatility:
            # чем выше цена, тем потенциально больше абсолютное отклонение,
            # но процент всё ещё из диапазона; можно добавлять адаптивность при необходимости
            pass

        # процент в диапазоне [-hi, -lo] U [lo, hi]
        sign = self._rand.choice([-1, 1])
        pct = round(self._rand.uniform(lo, hi) * sign, 4)  # округление до 4 знаков после запятой
        return pct

    def _apply_percent(self, price: Decimal, pct: float) -> Decimal:
        multiplier = Decimal(str(1 + pct / 100))
        new_price = (price * multiplier).quantize(Decimal(self.PRICE_QUANT), rounding=ROUND_HALF_UP)
        return new_price

    def _generate_launch_price_from_price(self, current_price: Decimal) -> Decimal:
        """
        Если текущая цена есть — генерируем launch_price как часть current_price
        ratio в [min_ratio, max_ratio]
        """
        ratio = self._rand.uniform(self.launch_config.min_ratio, self.launch_config.max_ratio)
        lp = (current_price * Decimal(str(ratio))).quantize(self.LAUNCH_PRICE_QUANT, rounding=ROUND_HALF_UP)
        return lp

    def _generate_launch_price_fallback(self) -> Decimal:
        lp = Decimal(str(self._rand.uniform(self.launch_config.fallback_min, self.launch_config.fallback_max)))
        return lp.quantize(self.LAUNCH_PRICE_QUANT, rounding=ROUND_HALF_UP)

    def generate(self, coin: Coin) -> Dict[str, object]:
        """
        Возвращает словарь: поля для обновления coin (не сохраняет).
        Логика:
          - если price пустой/ноль -> initial price (возможна стратегия based_on_market_cap)
          - иначе -> new_price = price * (1 + pct/100)
          - обновляем price_change_24h (процент) и high/low если нужно
        """
        out: Dict[str, object] = {}

        current_price = coin.price
        if current_price is None or float(current_price) == 0:
            # если стратегия based_on_market_cap — используем coin.market_cap для
            # определения начальной цены (примерная формула)
            if self.config.initial_strategy == "based_on_market_cap" and getattr(coin, "market_cap", None):
                # простая эвристика: price ≈ market_cap / circulating_supply (если есть)
                mc = coin.market_cap
                circ = getattr(coin, "circulating_supply", None) or getattr(coin, "total_supply", None)
                try:
                    if mc and circ and float(circ) > 0:
                        price = (self._decimal(mc) / self._decimal(circ)).quantize(self.PRICE_QUANT, rounding=ROUND_HALF_UP)
                    else:
                        price = self._initial_price()
                except Exception:
                    price = self._initial_price()
            else:
                price = self._initial_price()

            out["price"] = price
            # при инициализации не выставляем percent сразу (или ставим 0)
            out["price_change_24h"] = None
            out["high_24h_price"] = price if not getattr(coin, "high_24h_price", None) else coin.high_24h_price
            out["low_24h_price"] = price if not getattr(coin, "low_24h_price", None) else coin.low_24h_price
            return out

        # если цена есть — применяем волатильность
        price_dec = self._decimal(current_price)
        pct = self._percent_change(price_dec)
        new_price = self._apply_percent(price_dec, pct)

        out["price"] = new_price
        out["price_change_24h"] = float(round(pct, 6))  # храним в процентах, float ok
        out["price_change_1h"] = float(round(pct, 6))
        # обновляем high/low: note — это просто текущая тик-логика; можно иметь reset по 24h
        if not getattr(coin, "high_24h_price", None) or new_price > coin.high_24h_price:
            out["high_24h_price"] = new_price
        if not getattr(coin, "low_24h_price", None) or new_price < coin.low_24h_price:
            out["low_24h_price"] = new_price

        # --- 2. launch_price handling ---
        # Устанавливаем launch_price только если поле пустое/нулевое или если конфиг явно разрешает
        set_lp = False
        if getattr(coin, "launch_price", None) in (None, 0) or not self.launch_config.set_only_if_missing:
            set_lp = True

        if set_lp:
            # если есть текущая цена (только что обновлённая или существующая) — используем её
            base_price = out.get("price") or getattr(coin, "price", None)
            if base_price and float(base_price) > 0:
                launch_price = self._generate_launch_price_from_price(self._decimal(base_price))
            else:
                launch_price = self._generate_launch_price_fallback()

            out["launch_price"] = launch_price

        # Всё готово — возвращаем словарь
        return out
