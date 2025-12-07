import re
from django.core.management.base import BaseCommand
from app.models import Coin


class Command(BaseCommand):
    help = "Unpublish coins with invalid slug characters"

    # Разрешённые символы
    SLUG_PATTERN = re.compile(r'^[a-zA-Z0-9_-]+$')

    def handle(self, *args, **kwargs):
        bad_coins = []

        for coin in Coin.objects.all():
            if not self.SLUG_PATTERN.match(coin.slug):
                bad_coins.append(coin)

        if not bad_coins:
            self.stdout.write(self.style.SUCCESS("No problematic coins found."))
            return

        self.stdout.write(f"Found {len(bad_coins)} bad coins. Unpublishing...")

        for coin in bad_coins:
            coin.is_published = False
            coin.save(update_fields=["is_published"])
            self.stdout.write(f"Unpublished: {coin.id} — {coin.slug}")

        self.stdout.write(self.style.SUCCESS("Finished."))


# python manage.py unpublish_bad_slugs
# # nohup python manage.py unpublish_bad_slugs > unpublish_bad_slugs.log 2>&1 &