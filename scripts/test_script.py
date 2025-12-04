import os
import sys

from datetime import datetime, timezone, timedelta, date

# if __name__ == '__main__':
#     # Добавляем путь к корню проекта до импорта модулей
#     sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
#     import django
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')
#     django.setup()
#     from django.conf import settings
#     base_dir = settings.BASE_DIR
# else:
#     from django.conf import settings
#     base_dir = settings.BASE_DIR


# Разные форматы
signup_ts1 = "2025-11-14T15:00:00"          # ISO 8601, с T
signup_ts2 = "2025-11-14 15:00:00"          # с пробелом вместо T
signup_ts3 = "2025-11-14"                   # только дата, время будет 00:00:00
signup_ts4 = "2025-11-14T15:00"             # без секунд
signup_ts5 = "2025-11-14T15:00:00+03:00"    # с часовым поясом

# datetime с текущей датой и временем
signup_ts6 = datetime.now()   # текущая дата и время локальные
# datetime с конкретной датой и временем
signup_ts7 = datetime(year=2025, month=11, day=14, hour=15, minute=0, second=0)  # 14 ноября 2025, 15:00:00, без таймзоны
# datetime с часовым поясом
signup_ts8 = datetime(year=2025, month=11, day=14, hour=15, minute=0, second=0, tzinfo=timezone.utc)  # UTC
signup_ts9 = datetime(
    year=2025, month=11, day=14, hour=15, minute=0, second=0, tzinfo=timezone(timedelta(hours=3)) # +03:00
)
signup_ts11 = datetime(
    year=2025, month=11, day=14, hour=15, minute=0, second=0, microsecond=123456  # 15:00:00.123456
)
# только дата (time будет 00:00:00)
signup_ts10 = date(year=2025, month=11, day=14)  # 14 ноября 2025, time=00:00:00 автоматически

# external_data = {'id': 1, 'signup_ts': datetime.now(), 'tastes': {"a": 1}}



def main():
    from typing import Annotated, List, Any
    from pydantic import BaseModel, PositiveInt, ValidationError, Field, field_validator

    # Annotated = обычный тип + «инструкция» для библиотеки или инструментов.
    # В Pydantic это идеальный способ использовать свои валидаторы

    class Address(BaseModel):
        street: str
        city: str
        country: str

    class User(BaseModel):
        id: int
        # В контексте Field(...) троеточие (...) означает обязательное поле.
        name: str = Field(..., min_length=4, max_length=50)  # ограничение длины строки
        signup_ts: datetime | None
        address: Address | None

        tastes: dict[str, Annotated[int, PositiveInt]]
        # List[Annotated[str, Field(max_length=20)]]  -  каждый элемент ≤ 20 символов
        # Field(max_length=100)  -   список ≤ 100 элементов
        tags: Annotated[
            List[ Annotated[str, Field(max_length=20)] ],
            Field(max_length=100)
        ]
        # список не длиннее 10 элементов
        mixed_list: Annotated[List[Any], Field(max_length=10)]

        # Валидатор для одного поля
        @field_validator('name')
        def name_must_have_space(cls, value: str) -> str:
            if ' ' not in value:
                raise ValueError('Имя должно содержать пробел!')
            return value


    external_data = {
        'id': 1,
        'name':'Pasha Nebrat',
        'signup_ts': signup_ts3,
        'address': {
            'street': 'Pasha Nebrat',
            'city': 'New York',
            'country': 'United States',
        },
        'tastes': {"a": 1},
        'tags': ['sss', 'aaa', 'bbb', 'ccc', 'ddd'],
        'mixed_list': ['string', 102, 1.2, -3, -4.5, 'end']
    }

    try:
        user_data = User(**external_data)
        print(user_data)
    except ValidationError as e:
        print(e.errors())


if __name__ == '__main__':
    main()

