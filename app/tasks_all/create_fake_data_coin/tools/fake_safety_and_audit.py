import random
from datetime import date, timedelta

from app.models import SafetyAndAudit, AuditProvider, AuditStatus


class FakeSafetyAndAuditCreator:
    PROVIDERS = [
        "CertiK", "Hacken", "SlowMist", "Quantstamp", "Chainsulting",
        "Trail of Bits", "OpenZeppelin", "BlockSec", "Immunefi", "PeckShield"
    ]

    def __init__(self):
        # Получаем или создаём два статуса
        self.status_verified, _ = AuditStatus.objects.get_or_create(status="Verified")
        self.status_unverified, _ = AuditStatus.objects.get_or_create(status="Unverified")

        # Получаем или создаём 10 провайдеров
        self.providers = []
        for p in self.PROVIDERS:
            provider_obj, _ = AuditProvider.objects.get_or_create(provider=p)
            self.providers.append(provider_obj)

    def generate(self, coin):
        """
        Генерирует SafetyAndAudit запись для монеты.
        """

        # Проверяем, есть ли уже запись
        if hasattr(coin, "safety_and_audit"): return {}
        # Выбор статуса
        audit_status = random.choice([self.status_verified, self.status_unverified])
        # Provider — всегда один из списка
        audit_provider = random.choice(self.providers)
        # Логика безопасности:
        if audit_status.status == "Unverified":
            security_score = 0.0
        else:
            # 50.0 – 100.0
            security_score = round(random.uniform(50.0, 100.0), 2)
        # Случайная дата в пределах года назад
        last_date = date.today() - timedelta(days=random.randint(0, 365))

        SafetyAndAudit.objects.create(
            coin=coin,
            audit_status=audit_status,
            audit_provider=audit_provider,
            security_score=security_score,
            last_date=last_date
        )

        # Ничего не обновляется в Coin → возвращаем пустой dict
        return {}
