from dataclasses import dataclass
from typing import Optional


@dataclass
class PriceFakeConfig:
    # стратегия начальной цены: 'uniform', 'loguniform', 'based_on_market_cap'
    initial_strategy: str = "loguniform"

    # диапазон для initial_strategy (если применимо)
    initial_min: float = 0.0001
    initial_max: float = 1000.0

    # волатильность тика в процентах (abs value)
    volatility_min_percent: float = 0.1  # минимальное изменение в %
    volatility_max_percent: float = 3.0  # максимальное изменение в %

    # при вычислении процентов можно учитывать порядки величин цены
    scale_volatility: bool = True

    # seed для детерминированного поведения в тестах
    random_seed: Optional[int] = None


@dataclass
class LaunchPriceConfig:
    # доли от текущей цены для realistic launch_price, если price есть
    min_ratio: float = 0.01
    max_ratio: float = 0.5

    # fallback диапазон, если текущей цены нет
    fallback_min: float = 0.0001
    fallback_max: float = 1.0

    # если True — генерируем launch_price только если поле пустое или 0
    set_only_if_missing: bool = True
