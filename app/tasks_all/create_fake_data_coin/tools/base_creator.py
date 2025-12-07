from abc import ABC, abstractmethod
from typing import Dict
from app.db_models import Coin


class BaseFakeCreator(ABC):
    """
    Интерфейс: каждый генератор должен реализовать generate(coin) -> dict
    Возвращаемый dict — пары {field_name: value}, которые будут применены к объекту coin.
    Не сохраняет объект.
    """

    @abstractmethod
    def generate(self, coin: Coin) -> Dict[str, object]:
        raise NotImplementedError
