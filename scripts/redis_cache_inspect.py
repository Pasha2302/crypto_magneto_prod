import os
import sys
import json

if __name__ == '__main__':
    # Добавляем путь к корню проекта до импорта модулей
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')
    django.setup()
    from django.conf import settings
    base_dir = settings.BASE_DIR
else:
    from django.conf import settings
    base_dir = settings.BASE_DIR

from django.core.cache import cache


def list_keys(pattern="*"):
    client = cache.client.get_client()  # низкоуровневый redis-py клиент
    keys = client.keys(pattern)
    print(f"Found {len(keys)} keys:")
    for k in keys:
        print("-", k.decode())


def get_value(key):
    data = cache.get(key)
    print("Value:")
    try:
        print(json.dumps(data, indent=4, ensure_ascii=False))
    except:
        print(data)


def main():
    # Получаем все ключи кеша
    # Важно: если используешь django-redis, ключи хранятся с префиксом из settings.py
    keys = cache.keys('*')  # '*' — все ключи

    if not keys:
        print("Кеш пустой")
        return

    print(f"Всего ключей: {len(keys)}\n")

    for key in keys:
        value = cache.get(key)
        try:
            # Пробуем красиво распечатать словари/списки
            value_print = json.dumps(value, indent=2, ensure_ascii=False)
        except TypeError:
            value_print = str(value)
        print(f"Key: {key}\nValue:\n{value_print}\n{'-'*50}")

if __name__ == "__main__":
    main()