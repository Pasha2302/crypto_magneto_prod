from django.db import models
from django.utils.text import slugify


class BaseCoin(models.Model):
    """ Модель для хранения базовой информации о монетах. """
    slug = models.SlugField(max_length=255, unique=True, db_index=True, blank=True, null=True)
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=50)
    pair_url = models.URLField(max_length=500, blank=True, null=True)
    price = models.DecimalField(max_digits=64, decimal_places=18, blank=True, null=True)
    format_price = models.CharField(max_length=64, blank=True, null=True)

    objects = models.Manager()

    class Meta:
        ordering = ["id"]
        verbose_name = "Base Coin"
        verbose_name_plural = "Base Coins"

    def __str__(self):
        return self.name if self.name else ""

    def save(self, *args, **kwargs):
        # Автоматическое создание slug
        if self.name and self.symbol and not self.slug:
            self.slug = slugify(f"{self.name}-{self.symbol}", allow_unicode=True)
        super().save(*args, **kwargs)

