from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe

from app.admin_registration.admin_forms.widgets.image_file_input import ImageFileInput
from app.admin_registration.coin.inline_models.coin_inline import CoinSocialInline, SafetyAndAuditInline
from app.db_models import BaseCoin
from app.db_models.coin.coin_models import Coin, PromotedCoin


@admin.register(PromotedCoin)
class PromotedCoinsAdmin(admin.ModelAdmin):
    """
    Атрибуты:
        List_display (кортеж): поля, отображаемые в представлении списка в интерфейсе администратора.
        List_filter (кортеж): фильтруемые поля в представлении списка администратора для целевого поиска.
        Search_fields (кортеж): поля для поиска в интерфейсе администратора.

    Методы:
        get_queryset(request):
        возвращает оптимизированный набор запросов с предварительно загруженной связанной информацией о монетах.
    """
    list_display = ('coin', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('coin__name', 'coin__symbol')
    autocomplete_fields = ('coin',)

    formfield_overrides = {
        models.ImageField: {'widget': ImageFileInput},
    }

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('coin')


@admin.register(BaseCoin)
class BaseCoinAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', 'format_price', )
    formfield_overrides = {
        models.ImageField: {'widget': ImageFileInput},
    }


# ============================================================================================================= #

@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    change_form_template = 'app/admin/coin_temp/coin_change_form.html'
    list_display = (
        'id', 'display_image', 'name', 'symbol',
        'created_at', 'updated_at',
        'is_published',
    )
    list_display_links = ('name', 'symbol', )
    readonly_fields = (
        'pk', 'slug', 'format_price',
        'launch_date', 'published_at', 'created_at', 'updated_at',
    )

    fieldsets = (
        (None, {
            'fields': (
                'is_published', 'name', 'symbol', 'image', 'full_desc',
                'categories', 'labels',
            )
        }),
        ('Contract Address', {
            'fields': ('chain', 'contract_address',),
            'classes': ('contract-address-wrapp',)
        }),
        ('Market Metrics', {
            'fields': (
                'price', 'market_cap', 'liquidity_usd', 'volume_usd', 'volume_btc',
                'market_cap_presale',
            ),
            'classes': ('market-metrics-wrapp',)
        }),
        ('Readonly Fields', {
            'fields': readonly_fields,
            'classes': ('readonly-fields-wrapp',)
        }),
    )

    formfield_overrides = {
        models.ImageField: {'widget': ImageFileInput},
    }

    autocomplete_fields = ('chain',)
    search_fields = ('id', 'name', 'symbol', )   # 'contract_address__contract_address'
    list_editable = ('is_published', )  # Редактируемое поле в общем списке

    ordering = ['-created_at']  # Сортировка по убыванию — сначала новые
    list_filter = ('is_published', )  # Фильрация по полю в общем списке.

    inlines = (SafetyAndAuditInline, CoinSocialInline, )

    filter_horizontal = ('categories', 'labels', )

    def display_image(self, obj):
        if hasattr(obj, 'image'):
            img_url = obj.image.url if obj.image else None
            if img_url:
                return mark_safe(f'<img src="{img_url}" style="width: 60px; height: 60px;" />')
        return "No Image"
    display_image.short_description = 'Image'
