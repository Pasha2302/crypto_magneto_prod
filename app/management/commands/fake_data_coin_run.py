from django.core.management.base import BaseCommand

from app.db_models import Coin
from app.tasks_all.create_fake_data_coin.fake_data_starter import FakeDataCoinManager


class Command(BaseCommand):
    help = "Запуск задачи по установки фейковых данны для монет."

    def handle(self, *args, **options):
        # qs = Coin.objects.filter(symbol='DOGE')
        data = FakeDataCoinManager().run()

        self.stdout.write(self.style.SUCCESS(
            f"\nЗадачи по установки фейковых данны для монет. Выполнено ...\n"
            f"Return Data: {data}\n")
        )
        # self.stdout.write(self.style.SUCCESS(f"Задача завершена"))


# python manage.py fake_data_coin_run
# nohup python manage.py fake_data_coin_run > fake_data_coin_run.log 2>&1 &
