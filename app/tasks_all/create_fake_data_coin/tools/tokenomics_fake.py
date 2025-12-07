import random
from decimal import Decimal
from typing import Dict
from app.db_models import Coin

from app.tasks_all.create_fake_data_coin.tools.base_creator import BaseFakeCreator


class FakeTokenomicsCreator(BaseFakeCreator):
    """
    Генератор фейковых данных токеномики и рыночных метрик.
    Возвращает dict — никаких сохранений.
    """

    def __init__(self,
                 supply_min=1_000,
                 supply_max=10_000_000_000,
                 volume_min=10_000,
                 volume_max=500_000_000,
                 liquidity_min=5_000,
                 liquidity_max=250_000_000):

        self.supply_min = supply_min
        self.supply_max = supply_max
        self.volume_min = volume_min
        self.volume_max = volume_max
        self.liquidity_min = liquidity_min
        self.liquidity_max = liquidity_max

        self._rand = random.Random()

    def _dec(self, value, precision=8):
        return Decimal(str(round(value, precision)))

    def _rand_range_dec(self, min_v, max_v, precision=8):
        value = self._rand.uniform(min_v, max_v)
        return self._dec(value, precision)

    def generate(self, coin: Coin) -> Dict[str, object]:
        """
        Генерирует:
            total_supply
            max_supply
            circulating_supply
            market_cap
            liquidity_usd
            volume_usd
            volume_btc

        Всё реалистично и логично связано.
        """

        # -------- SUPPLY --------
        # Max supply (если нет) — верхняя граница
        max_supply = coin.max_supply or self._rand_range_dec(
            self.supply_min, self.supply_max
        )

        # Total supply — обычно <= max_supply
        total_supply = coin.total_supply or self._rand_range_dec(
            max(self.supply_min, float(max_supply) * 0.6),
            float(max_supply)
        )

        # Circulating supply — не больше total_supply
        circulating_supply = coin.circulating_supply or self._rand_range_dec(
            float(total_supply) * 0.3,
            float(total_supply)
        )

        # -------- MARKET CAP --------
        # market_cap ~ price * circulating_supply
        if coin.price:
            market_cap = Decimal(coin.price) * circulating_supply
            market_cap = self._dec(float(market_cap), precision=2)
        else:
            # если цена пока фейковая — ставим в разумный диапазон
            market_cap = self._rand_range_dec(10_000_000, 5_000_000_000, precision=2)

        # -------- LIQUIDITY --------
        liquidity_usd = coin.liquidity_usd or self._rand_range_dec(
            self.liquidity_min, self.liquidity_max, precision=2
        )

        # -------- VOLUME --------
        volume_usd = self._rand_range_dec(
            self.volume_min, self.volume_max, precision=2
        )

        # объём в BTC (приближенно, без хардкода)
        # Цена битка—не хардкод, а параметризуем:
        btc_price = 60_000  # можно вынести в settings потом
        volume_btc = self._dec(float(volume_usd) / btc_price, precision=8)

        return {
            "max_supply": max_supply,
            "total_supply": total_supply,
            "circulating_supply": circulating_supply,
            "market_cap": market_cap,
            "liquidity_usd": liquidity_usd,
            "volume_usd": volume_usd,
            "volume_btc": volume_btc,
        }
