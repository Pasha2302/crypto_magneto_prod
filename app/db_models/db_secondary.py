from django.db import models
import pycountry   # uv add pycountry
from django.utils.text import slugify


class Country(models.Model):
    slug = models.SlugField(max_length=255, unique=True, db_index=True,)
    name = models.CharField(max_length=255, unique=True, verbose_name="Country Name", blank=True, null=True)
    code_alpha_2 = models.CharField(max_length=2, unique=True, db_index=True, blank=True, null=True)
    code_alpha_3 = models.CharField(max_length=3, unique=True, db_index=True, blank=True, null=True)
    emoji_flag = models.CharField(max_length=4, blank=True, null=True)
    flag = models.ImageField(upload_to='country_flags/', blank=True, null=True)

    # 🔥 Новое поле — как пришло с сайта
    raw_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Raw Country Name")

    class Meta:
        ordering = ["id"]
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        emj = f"{self.emoji_flag} " if self.emoji_flag else ""
        _str = self.name or self.raw_name or "Unknown"
        return f"{emj}{_str}"

    def save(self, *args, **kwargs):
        # если slug не указан — выставляем автоматически
        if not self.slug and (self.name or self.raw_name):
            base_name = self.name if self.name else self.raw_name
            self.slug = slugify(base_name)
        super().save(*args, **kwargs)

    @staticmethod
    def country_to_emoji(alpha_2_code):
        # Преобразуем код страны в эмодзи флага
        return ''.join(chr(127397 + ord(c)) for c in alpha_2_code.upper())

    @classmethod
    def import_countries(cls):
        for country in pycountry.countries:
            emoji_flag = cls.country_to_emoji(country.alpha_2) if len(country.alpha_2) == 2 else None

            # Создаем запись или обновляем существующую
            cls.objects.update_or_create(
                code_alpha_2=country.alpha_2,
                defaults={
                    'name': country.name,
                    'slug':  slugify(country.name),
                    'code_alpha_3': country.alpha_3,
                    'emoji_flag': emoji_flag,
                }
            )

