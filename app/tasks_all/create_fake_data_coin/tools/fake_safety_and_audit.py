import random
from datetime import date, timedelta
from decimal import Decimal

from app.models import SafetyAndAudit, AuditProvider, AuditStatus


class FakeSafetyAndAuditCreator:
    PROVIDERS = [
        "CertiK", "Hacken", "SlowMist", "Quantstamp", "Chainsulting",
        "Trail of Bits", "OpenZeppelin", "BlockSec", "Immunefi", "PeckShield"
    ]

    def __init__(self):
        # Получаем или создаём статусы
        self.status_verified, _ = AuditStatus.objects.get_or_create(status="Verified")
        self.status_unverified, _ = AuditStatus.objects.get_or_create(status="Unverified")

        # Получаем провайдеров
        self.providers = [
            AuditProvider.objects.get_or_create(provider=p)[0]
            for p in self.PROVIDERS
        ]

    @staticmethod
    def _score_market_cap(cap: Decimal | None) -> float:
        """0 → 0.6  (60% влияния)"""
        if not cap:
            return 0.05

        cap = float(cap)

        if cap > 1_000_000_000:  # > 1B
            return 0.6
        elif cap > 100_000_000:
            return 0.45
        elif cap > 10_000_000:
            return 0.3
        elif cap > 1_000_000:
            return 0.15
        return 0.05

    def _score_volume(self, volume: Decimal | None) -> float:
        """0 → 0.2 (20% влияния)"""
        if not volume:
            return 0.02

        v = float(volume)

        if v > 50_000_000:
            return 0.2
        elif v > 10_000_000:
            return 0.12
        elif v > 1_000_000:
            return 0.06
        return 0.03

    def _score_age(self, coin) -> float:
        """0 → 0.2 (20% влияния)"""
        launch_date = getattr(coin, "launch_date", None)
        if not launch_date:
            return 0.03  # если нет данных — маленький бонус

        days = (date.today() - launch_date).days

        if days > 3 * 365:
            return 0.2
        elif days > 2 * 365:
            return 0.15
        elif days > 1 * 365:
            return 0.1
        return 0.03

    def _calculate_verified_probability(self, coin) -> float:
        """Общая вероятность от 0 до 1"""
        p = 0.0
        p += self._score_market_cap(getattr(coin, "market_cap", None))
        p += self._score_volume(getattr(coin, "volume_usd", None))
        p += self._score_age(coin)

        # лёгкая случайность ± 5%
        p += random.uniform(-0.05, 0.05)
        # ограничиваем [0,1]
        return max(0.0, min(1.0, p))

    def generate(self, coin):
        """
        Создаёт или обновляет SafetyAndAudit запись.
        """

        # === 1. Вычисляем вероятность Verified ===
        probability = self._calculate_verified_probability(coin)
        # print(probability)  # можно включить для тестов

        audit_status = (
            self.status_verified
            if random.random() < probability
            else self.status_unverified
        )

        # === 2. Остальные поля ===
        audit_provider = random.choice(self.providers)
        if audit_status.status == "Unverified":
            security_score = 0.0
        else:
            # Чем выше вероятность Verified → тем выше средний security_score
            base = 50 + probability * 40  # 50–90
            security_score = round(random.uniform(base, 100.0), 2)

        last_date = date.today() - timedelta(days=random.randint(0, 365))

        # === 3. Создаём или обновляем ===
        if hasattr(coin, "safety_and_audit"):
            sa = coin.safety_and_audit
            sa.audit_status = audit_status
            sa.audit_provider = audit_provider
            sa.security_score = security_score
            sa.last_date = last_date
            sa.save()
        else:
            SafetyAndAudit.objects.create(
                coin=coin,
                audit_status=audit_status,
                audit_provider=audit_provider,
                security_score=security_score,
                last_date=last_date
            )

        return {}
