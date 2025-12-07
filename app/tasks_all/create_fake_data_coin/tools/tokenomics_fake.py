import random
from decimal import Decimal
from typing import Dict

from app.db_models import Coin
from app.tasks_all.create_fake_data_coin.tools.base_creator import BaseFakeCreator


class FakeTokenomicsCreator(BaseFakeCreator):
    """
    Генератор фейковых данных токеномики и рыночных метрик.
    Возвращает dict — не сохраняет объект Coin.
    """

    # Hard safety caps (защита, но НЕ часть логики)
    MAX_MARKET_CAP = Decimal("9000000000000")   # 9e11 — предел DecimalField
    MAX_LIQUIDITY = Decimal("250000000")       # 2.5e8
    MAX_VOLUME = Decimal("500000000")          # 5e8

    BTC_PRICE = Decimal("60000")

    def __init__(
        self,
        supply_min=1_000,
        supply_max=10_000_000_000,
        volume_min=10_000,
        volume_max=500_000_000,
        liquidity_min=5_000,
        liquidity_max=250_000_000,
    ):
        self.supply_min = Decimal(supply_min)
        self.supply_max = Decimal(supply_max)
        self.volume_min = Decimal(volume_min)
        self.volume_max = Decimal(volume_max)
        self.liquidity_min = Decimal(liquidity_min)
        self.liquidity_max = Decimal(liquidity_max)

        self._rand = random.Random()

    # Helpers
    @staticmethod
    def _dec(value: Decimal, precision=8) -> Decimal:
        """Безопасное приведение к Decimal с округлением."""
        return value.quantize(Decimal(10) ** -precision)

    def _rand_range_dec(self, min_v: Decimal, max_v: Decimal, precision=8) -> Decimal:
        """Случайный Decimal из диапазона."""
        value = Decimal(str(self._rand.uniform(float(min_v), float(max_v))))
        return self._dec(value, precision)

    def _cap(self, value: Decimal, limit: Decimal, precision=2) -> Decimal:
        """Устанавливаем лимит, но не ломаем распределение."""
        if value > limit: value = Decimal(str(
            self._rand.uniform(float(limit - 1_000_000_000), float(limit))
        ))
        value = min(value, limit)
        return self._dec(value, precision)

    # GENERATOR
    def generate(self, coin: Coin) -> Dict[str, object]:
        """
        total_supply
        max_supply
        circulating_supply
        market_cap
        liquidity_usd
        volume_usd
        volume_btc
        """

        # SUPPLY
        max_supply = (
            Decimal(coin.max_supply)
            if coin.max_supply
            else self._rand_range_dec(self.supply_min, self.supply_max)
        )

        total_supply = (
            Decimal(coin.total_supply)
            if coin.total_supply
            else self._rand_range_dec(max_supply * Decimal("0.6"), max_supply)
        )

        circulating_supply = (
            Decimal(coin.circulating_supply)
            if coin.circulating_supply
            else self._rand_range_dec(total_supply * Decimal("0.3"), total_supply)
        )

        # -----------------------------
        # MARKET CAP
        # -----------------------------
        if coin.price:
            market_cap = Decimal(coin.price) * circulating_supply
            market_cap = self._cap(market_cap, self.MAX_MARKET_CAP, precision=2)

        else:
            # Цена неизвестна -> генерим реальный диапазон
            market_cap = self._rand_range_dec(
                Decimal("10000000"),      # 10M
                Decimal("5000000000"),    # 5B
                precision=2
            )
            market_cap = self._cap(market_cap, self.MAX_MARKET_CAP)

        # LIQUIDITY
        liquidity_usd = (
            Decimal(coin.liquidity_usd)
            if coin.liquidity_usd
            else self._rand_range_dec(self.liquidity_min, self.liquidity_max, precision=2)
        )
        liquidity_usd = self._cap(liquidity_usd, self.MAX_LIQUIDITY)

        # VOLUME
        volume_usd = self._rand_range_dec(self.volume_min, self.volume_max, precision=2)
        volume_usd = self._cap(volume_usd, self.MAX_VOLUME)
        volume_btc = self._dec(volume_usd / self.BTC_PRICE, precision=8)

        return {
            "max_supply": max_supply,
            "total_supply": total_supply,
            "circulating_supply": circulating_supply,
            "market_cap": market_cap,
            "liquidity_usd": liquidity_usd,
            "volume_usd": volume_usd,
            "volume_btc": volume_btc,
        }
