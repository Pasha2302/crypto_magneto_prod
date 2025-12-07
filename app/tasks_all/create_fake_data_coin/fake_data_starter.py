import logging
from django.db import transaction
from app.db_models import Coin
from .tools.fake_safety_and_audit import FakeSafetyAndAuditCreator
from .tools.prediction_fake import FakePredictionCreator
from .tools.price_fake import PriceFakeCreator
from .tools.config import PriceFakeConfig, LaunchPriceConfig
from .tools.tokenomics_fake import FakeTokenomicsCreator

logger = logging.getLogger("app.tasks_all")

price_cfg = PriceFakeConfig(
    initial_strategy="loguniform",
    initial_min=0.00001,
    initial_max=5000.0,
    volatility_min_percent=0.05,
    volatility_max_percent=5.0,
    random_seed=None
)

launch_cfg = LaunchPriceConfig(
    min_ratio=0.01,
    max_ratio=0.5,
    fallback_min=0.0001,
    fallback_max=1.0,
    set_only_if_missing=True
)

class FakeDataCoinManager:
    def __init__(self, fetch_qs=None, creators=None):
        # можно передать queryset или использовать все опубликованные
        self.qs_coins = fetch_qs if fetch_qs is not None else Coin.objects.filter(is_published=True)
        # creators — список инстансов BaseFakeCreator
        self.creators = creators if creators is not None else [
            FakeTokenomicsCreator(),
            PriceFakeCreator(price_cfg, launch_cfg),
            FakePredictionCreator(),
            FakeSafetyAndAuditCreator(),
        ]

    def run(self):
        logger.info("Starting fake data generation; count=%s", self.qs_coins.count())
        for coin in self.qs_coins:
            try:
                self._process_coin(coin)
            except Exception as exc:
                logger.exception("Failed to process coin %s: %s", coin.slug, exc)

    def _process_coin(self, coin):
        # собираем все изменения в одну транзакцию
        update_data = {}
        for creator in self.creators:
            data = creator.generate(coin)
            if data:
                update_data.update(data)

        if not update_data:
            return

        # Применяем изменения и сохраняем в транзакции
        try:
            with transaction.atomic():
                for field, value in update_data.items():
                    setattr(coin, field, value)
                coin.save()
            # logger.info("Updated coin %s with fields: %s", coin.slug, list(update_data.keys()))
        except Exception as exc:
            logger.exception("Error saving coin %s: %s", coin.slug, exc)
            raise



