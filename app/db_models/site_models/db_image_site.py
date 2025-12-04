from django.db import models
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFit


class ImageSocial(models.Model):
    SCHEME = (
        ('dark', 'Dark'),
        ('light', 'Light'),
    )
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    usage = models.CharField(max_length=100, blank=True, default='')
    scheme = models.CharField(max_length=10, choices=SCHEME, default='dark')

    image = models.ImageField(upload_to='site_images/social', )
    # Миниатюры для адаптивного отображения
    img_64 = ImageSpecField(
        source='image',
        processors=[ResizeToFit(width=64, height=64)],
        format='WEBP',
        options={'quality': 80}
    )

    class Meta:
        ordering = ['pk']
        verbose_name_plural = 'images Social'

    def __str__(self):
        return self.name if self.name else f'Image Social ({self.pk})'

    def save(self, *args, **kwargs):
        if self.name and not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


class ImageSite(models.Model):
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    name = models.CharField(max_length=255, verbose_name="Image Name")
    name_page = models.CharField(max_length=255, verbose_name="Image Name Page")

    # Главное изображение
    image = models.ImageField(
        upload_to="site_images",
        max_length=255,
        blank=True,
        null=True
    )
    # Миниатюры для адаптивного отображения
    img_64 = ImageSpecField(
        source='image',
        processors=[ResizeToFit(width=64, height=64)],
        format='WEBP',
        options={'lossless': True}  # Без потери качества.
    )
    img_140 = ImageSpecField(
        source='image',
        processors=[ResizeToFit(width=140)],
        format='WEBP',
        options={'quality': 80}
    )
    img_240 = ImageSpecField(
        source='image',
        processors=[ResizeToFit(width=240)],
        format='WEBP',
        options={'quality': 80}
    )
    img_360 = ImageSpecField(
        source='image',
        processors=[ResizeToFit(width=360)],
        format='WEBP',
        options={'quality': 80}
    )
    img_640 = ImageSpecField(
        source='image',
        processors=[ResizeToFit(width=640)],
        format='WEBP',
        options={'quality': 85}
    )

    def save(self, *args, **kwargs):
        if self.name and self.name_page and not self.slug:
            self.slug = slugify(f"{self.name}-{self.name_page}")

        super().save(*args, **kwargs)
