from urllib.parse import urljoin

from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFit

from app.db_models.site_models import ImageSocial
from app.db_models.tools.format_price import normalized_price_coin
# from imagekit.models import ImageSpecField  # uv add django-imagekit

from app.db_models.tools.set_media_path import default_image_upload_path


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if self.name and not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Label(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Labels"

    def save(self, *args, **kwargs):
        if self.name and not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ============================================================================================================== #

class PromotedCoin(models.Model):
    """
    Модель для хранения информации о продвигаемых монетах.
    """
    coin = models.OneToOneField("Coin", on_delete=models.CASCADE, related_name='promoted')
    start_date = models.DateTimeField(default=timezone.now, null=True, blank=True,)
    end_date = models.DateTimeField(null=True, blank=True,)
    is_permanent = models.BooleanField(default=False, verbose_name="Promotion is Permanent")

    class Meta:
        ordering = ["id"]
        verbose_name = "Promoted Coin"
        verbose_name_plural = "Promoted Coin"

    def __str__(self):
        return f"Promoted: {self.coin.name} from {self.start_date} to {self.end_date}"


# ============================================================================================================== #

class ExplorerChain(models.Model):
    slug = models.SlugField(max_length=120, unique=True)
    name = models.CharField(max_length=50)
    url = models.URLField()

    class Meta:
        ordering = ["id"]
        verbose_name = "Explorer Chain"
        verbose_name_plural = "Explorer Chains"

    def __str__(self):
        return_str = ''
        if self.name: return_str = self.name
        return return_str

    def save(self, *args, **kwargs):
        if self.name and not self.slug: self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Chain(models.Model):
    slug = models.SlugField(max_length=255, unique=True, db_index=True, blank=True)
    name = models.CharField(max_length=50)
    image = models.FileField(upload_to='chain_images/', max_length=255, blank=True, null=True)
    symbol = models.CharField(max_length=50, unique=True, db_index=True, blank=True, null=True)

    explorer = models.OneToOneField(
        ExplorerChain, on_delete=models.SET_NULL, null=True, blank=True, related_name="chain"
    )

    class Meta:
        ordering = ["id"]

    def save(self, *args, **kwargs):
        if self.name and not self.slug: self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CoinSocial(models.Model):
    SOCIAL_CHOICES = [
        ('facebook', 'Facebook'),
        ('whitepaper', 'Whitepaper'),

        ('reddit', 'Reddit'),
        ('twitter', 'Twitter(X)'),
        ('gecko', 'Gecko'),
        ('discord', 'Discord'),
        ('market', 'Market'),
        ('website', 'Website'),
        ('github', 'GitHub'),
        ('youtube', 'YouTube'),
        ('tiktok', 'TikTok'),
        ('medium', 'Medium'),
        ('instagram', 'Instagram'),
        ('telegram', 'Telegram'),
    ]

    coin = models.ForeignKey('Coin', on_delete=models.CASCADE, related_name="socials")

    name = models.CharField(max_length=50, choices=SOCIAL_CHOICES, blank=True, null=True, )
    url = models.CharField(max_length=500, blank=True, null=True)
    image = models.ForeignKey(ImageSocial, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True, )

    class Meta:
        ordering = ["id"]
        verbose_name = "Socials"
        verbose_name_plural = "Socials"

    def __str__(self):
        return_str = ''
        if self.name: return_str = self.name
        return return_str


# ======================================  SafetyAndAudit  =========================================================== #
class AuditStatus(models.Model):
    status = models.CharField()
    def __str__(self):
        return self.status

class AuditProvider(models.Model):
    provider = models.CharField()
    def __str__(self):
        return self.provider

class SafetyAndAudit(models.Model):
    coin = models.OneToOneField('Coin', on_delete=models.CASCADE, related_name='safety_and_audit')
    audit_status = models.ForeignKey(AuditStatus, on_delete=models.CASCADE)
    audit_provider = models.ForeignKey(AuditProvider, on_delete=models.CASCADE)
    security_score = models.FloatField(blank=True, null=True)
    last_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ('pk',)
        verbose_name_plural = 'Safety And Audit'

    def __str__(self):
        return self.coin.name if self.coin else ''


class CoinPrediction(models.Model):
    CONFIDENCE_CHOICES = [
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    ]

    coin = models.ForeignKey("Coin", on_delete=models.CASCADE, related_name="predictions")
    year = models.PositiveIntegerField()
    min_price = models.DecimalField(max_digits=20, decimal_places=2)
    avg_price = models.DecimalField(max_digits=20, decimal_places=2)
    max_price = models.DecimalField(max_digits=20, decimal_places=2)

    confidence = models.CharField(
        max_length=10,
        choices=CONFIDENCE_CHOICES,
        default="medium"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at',)
        verbose_name_plural = 'Coin Predictions'

    def __str__(self):
        return f"Prediction price {self.coin.name}" if self.coin else 'Prediction price'


class TeamCoin(models.Model):
    name = models.CharField(max_length=50)
    job_title = models.CharField(max_length=50)

    image = models.ImageField(
        upload_to=default_image_upload_path,
        max_length=255,
        blank=True,
        null=True
    )
    img_64 = ImageSpecField(
        source='image',
        processors=[ResizeToFit(width=64, height=64)],
        format='WEBP',
        options={'lossless': True}  # Без потери качества.
    )

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Team Coins'

    def __str__(self):
        return f"{self.name} {self.job_title}"


# =================================================================================================================== #

class Coin(models.Model):
    # Основная информация
    slug = models.SlugField(max_length=150, unique=True)
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=20)

    contract_address = models.CharField(max_length=128, null=True)
    chain = models.ForeignKey(Chain, on_delete=models.CASCADE, related_name="coin", null=True)
    full_desc = models.TextField(blank=True, null=True, verbose_name="Full Description")
    views = models.IntegerField(blank=True, null=True)

    # Изображение монеты
    image = models.ImageField(
        upload_to=default_image_upload_path,
        max_length=255,
        blank=True,
        null=True
    )
    img_64 = ImageSpecField(
        source='image',
        processors=[ResizeToFit(width=64, height=64)],
        format='WEBP',
        options={'lossless': True}  # Без потери качества.
    )

    # ManyToManyField
    categories = models.ManyToManyField(Category, related_name="coins", blank=True)
    labels = models.ManyToManyField(Label, related_name="coins", blank=True)
    team = models.ManyToManyField(
        TeamCoin,
        related_name="coins",
        blank=True,
        help_text="Команда проекта"
    )

    # Метрики рынка (с nullable там, где данные могут отсутствовать)
    market_cap_presale = models.BooleanField(default=False)

    format_price = models.CharField(max_length=50, blank=True, null=True)
    price = models.DecimalField(max_digits=30, decimal_places=18, blank=True, null=True)
    price_change_24h = models.FloatField(blank=True, null=True)
    price_change_1h = models.FloatField(blank=True, null=True)
    high_24h_price = models.DecimalField(max_digits=30, decimal_places=18, null=True)
    low_24h_price = models.DecimalField(max_digits=30, decimal_places=18, null=True)

    market_cap = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    liquidity_usd = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

    volume_usd = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    volume_btc = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)

    # -------------------------------
    # TOKENOMICS & SUPPLY
    # -------------------------------

    # Total Supply — общее количество монет, созданных на данный момент.
    # Может меняться у некоторых монет, но нечасто.
    total_supply = models.DecimalField(
        max_digits=30, decimal_places=8,
        null=True, blank=True,
        help_text="Общее количество существующих монет на данный момент"
    )

    # Max Supply — максимальное количество монет, которое когда-либо может существовать.
    # Например, для Bitcoin = 21 000 000
    max_supply = models.DecimalField(
        max_digits=30, decimal_places=8,
        null=True, blank=True,
        help_text="Максимально возможное количество монет (лимит эмиссии)"
    )

    # Circulating Supply — количество монет в свободном обращении сейчас.
    # Меняется почти каждый день.
    circulating_supply = models.DecimalField(
        max_digits=30, decimal_places=8,
        null=True, blank=True,
        help_text="Количество монет, находящихся в обращении"
    )

    # Launch Price — цена монеты в момент запуска.
    launch_price = models.DecimalField(
        max_digits=20, decimal_places=8,
        null=True, blank=True,
        help_text="Цена монеты на момент запуска"
    )

    # Даты
    launch_date = models.DateField(
        null=True, blank=True,
        help_text="Дата запуска монеты"
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    last_price_update = models.DateTimeField(blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)

    is_published = models.BooleanField(default=False)

    @property
    def fdmc_computed(self):
        # Получить Fully Diluted Market Cap:
        if self.price and self.max_supply:
            return self.price * self.max_supply
        return None

    # ===================================================================================== #
    class Meta:
        ordering = ('pk',)
        verbose_name_plural = 'Coins'

    def get_site_url(self, is_relative_path: bool = False) -> str | None:
        """
            Возвращает относительный путь на страницу монеты если is_relative_path = True,
            иначе полный путь.
            Если slug_url отсутствует и не может быть создан, возвращает id монеты в виде строки.
        """
        BASE_SITE_URL = settings.BASE_SITE_URL

        # Проверяем slug_url
        coin_slug = self.slug
        if not coin_slug and self.name and self.symbol:
            coin_slug = slugify(f"{self.name}-{self.symbol}")
        if not coin_slug:
            # Если не удалось создать slug, возвращаем id
            return str(self.pk)

        try:
            relative_path = reverse(viewname="coin_page_view", kwargs={
                "chain_symbol": self.chain.symbol.lower(),
                "coin_slug": coin_slug
            })
        except Exception:
            # Если reverse по какой-то причине не сработал
            return str(self.pk)

        return relative_path if is_relative_path else urljoin(BASE_SITE_URL, relative_path)

    def update_publication_time(self):
        # Обновляем время публикации при изменении статуса
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        elif not self.is_published:
            self.published_at = None  # Сбрасываем время публикации, если монета снята с публикации

    def save(self, *args, **kwargs):
        self.update_publication_time()
        # Автоматическое создание slug
        if self.name and self.symbol and not self.slug:
            self.slug = slugify(f"{self.name}-{self.symbol}", allow_unicode=True)
        # Если монета в пресейле, сбрасываем market_cap
        if self.market_cap_presale:
            self.market_cap = None
        if self.price is not None:
            normalized_price_coin(self)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


