from django.db import models
from django.core.exceptions import ValidationError


class SiteSettings(models.Model):
    """
    Модель для хранения настроек Телеграмм Бота. Разрешена только одна запись.
    """
    token = models.CharField()

    class Meta:
        verbose_name = "App Settings"
        verbose_name_plural = "App Settings"

    def save(self, *args, **kwargs):
        if not self.pk and SiteSettings.objects.exists():
            raise ValidationError('Можно создать только одну запись Site Settings')
        return super().save(*args, **kwargs)

    def __str__(self):
        return "Settings"

