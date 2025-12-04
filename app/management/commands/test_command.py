from django.core.management.base import BaseCommand


def test_function():
    print("test_function")


class Command(BaseCommand):
    help = "Тестовый запуск задачи test_command"

    def handle(self, *args, **options):
        test_function()
        self.stdout.write(self.style.SUCCESS(f"Задача завершена"))

        # result = test_function.delay()  # запускаем как Celery задачу
        # self.stdout.write(self.style.SUCCESS(f"Задача отправлена в Celery, ID: {result.id}"))


# python manage.py test_command

# nohup python manage.py test_command > trends.log 2>&1 &

# nohup — не убьётся при выходе из терминала.
# > trends.log — весь stdout в файл.
# 2>&1 — ошибки (stderr) тоже туда.
# & — запуск в фоне.

# 🔎 Найти процесс:
# >> ps aux | grep test_command
# Или более удобно (PID + команда)
# >> pgrep -a -f test_command

# Остановить процесс по PID (замени 12345 на настоящий PID)
# >> kill 12345
# Если не убился обычным kill
# >> kill -9 12345
# Убить сразу все процессы с этим именем
# >> pkill -f test_command
