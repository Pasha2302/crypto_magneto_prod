import re
from decimal import Decimal, InvalidOperation


def format_decimal_number(number: Decimal) -> str | None:
    """
    Форматирует десятичное число для отображения.
    Убирает лишние нули и обрабатывает числа в экспоненциальной форме.
    """
    if number is None:
        return None

    # Преобразуем число в строку в обычном формате, избегая экспоненты
    number_str = format(number.normalize(), 'f')  # 'f' для полной записи числа
    # Если при нормализации число стало очень малым (например, 0), преобразуем в строку
    if number == 0:
        return "0.0"

    # Проверяем наличие дробной части
    if '.' in number_str:
        integer_part, fractional_part = number_str.split('.')
        try:
            # Проверяем, содержит ли дробная часть только нули
            fractional_decimal = Decimal(f"0.{fractional_part}")
            if fractional_decimal == 0:
                # print(f"{integer_part=}")
                return str(integer_part) or "0.0"

            # Считаем ведущие нули в дробной части
            first_non_zero_idx = len(fractional_part) - len(fractional_part.lstrip('0'))
            zero_count = first_non_zero_idx

            # Обрабатываем случай большого количества начальных нулей в дробной части
            if zero_count >= 3:
                significant_part = fractional_part[first_non_zero_idx: first_non_zero_idx + 2]
                return f"{integer_part}.|{zero_count}|{significant_part}"
            else:
                # Округляем до 3-х знаков дробной части, если это не особый случай
                rounded_number = Decimal(number).quantize(Decimal("0.001"))
                # print(f"{rounded_number=}")
                return str(rounded_number)
        except (InvalidOperation, ValueError):
            return number_str  # Если ошибка в обработке, возвращаем исходное число
    else:
        # Если у числа нет дробной части, возвращаем его как есть
        return number_str


def normalized_price_coin(coin):
    """Возвращает нормализованную цену."""
    if coin.price is not None:
        coin_price = Decimal(coin.price)
        formatted_price = format_decimal_number(coin_price)
        # print("\n\nFormatted Price: ", formatted_price)
        if formatted_price is not None and len(formatted_price) > 5:
            # Оставляем только 2 десятичных знака
            formatted_price = re.sub(r"(\.\d\d)[0-9]*$", r"\1", formatted_price)
            # Убираем лишние конечные нули
            formatted_price = re.sub(r"(\.\d*?[1-9])0+$", r"\1", formatted_price)

        coin.format_price = formatted_price
    else:
        coin.format_price = None
