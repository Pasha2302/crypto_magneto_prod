import random
from decimal import Decimal
from django.utils import timezone

from app.db_models import Coin
from app.tasks_all.create_fake_data_coin.tools.base_creator import BaseFakeCreator


class FakePredictionCreator(BaseFakeCreator):
    """
    Генерирует прогнозы цены на 3 года вперёд.
    Возвращает:
        { "predictions": [ {...}, {...}, {...} ] }
    """

    YEAR_SPAN = 3

    # volatility_ranges[year_offset] = (min%, max%)
    VOLATILITY = {
        1: (0.10, 0.30),   # 10–30% → высокая точность
        2: (0.20, 0.60),   # 20–60% → средняя
        3: (0.40, 1.20),   # 40–120% → низкая точность
    }

    CONFIDENCE = {
        1: "high",
        2: "medium",
        3: "low",
    }

    def __init__(self, seed: int | None = None):
        self._rand = random.Random(seed)

    @staticmethod
    def _dec(value, quant="0.01"):
        return Decimal(str(value)).quantize(Decimal(quant))

    def _make_year_prediction(self, base_price: Decimal, year_offset: int, target_year: int):
        lo, hi = self.VOLATILITY[year_offset]

        # drift всегда Decimal
        drift = Decimal(str(self._rand.uniform(lo, hi)))
        one = Decimal("1")

        # min
        min_price = base_price * (one - drift)

        # avg (случайное отклонение внутри ± drift/2)
        half_drift = drift / Decimal("2")
        rand_delta = Decimal(str(self._rand.uniform(float(-half_drift), float(half_drift))))
        avg_price = base_price * (one + rand_delta)

        # max
        max_price = base_price * (one + drift * Decimal("1.5"))

        return {
            "year": target_year,
            "min_price": self._dec(min_price),
            "avg_price": self._dec(avg_price),
            "max_price": self._dec(max_price),
            "confidence": self.CONFIDENCE[year_offset],
        }

    def generate(self, coin: Coin) -> None:
        """
        Генерирует и сохраняет прогнозы прямо в CoinPrediction.
        Не возвращает данные в update_data.
        """
        from app.db_models import CoinPrediction  # чтобы избежать циклического импорта

        if not coin.price:
            return None
        # --- Если уже есть прогнозы — выходим ---
        if coin.predictions.exists():
            return None

        base_price = Decimal(str(coin.price))
        current_year = timezone.now().year

        predictions = []

        for offset in range(1, self.YEAR_SPAN + 1):
            target_year = current_year + offset
            pred = self._make_year_prediction(base_price, offset, target_year)

            predictions.append(
                CoinPrediction(
                    coin=coin,
                    year=target_year,
                    min_price=pred["min_price"],
                    avg_price=pred["avg_price"],
                    max_price=pred["max_price"],
                    confidence=pred["confidence"],
                )
            )

        # Массовое создание
        CoinPrediction.objects.bulk_create(predictions)
        return None

