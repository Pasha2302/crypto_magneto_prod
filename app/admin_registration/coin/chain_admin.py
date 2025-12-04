from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from app.admin_registration.admin_forms.widgets.image_file_input import ImageFileInput
from app.db_models import Chain, ExplorerChain


@admin.register(ExplorerChain)
class ExplorerChainAdmin(admin.ModelAdmin):
    search_fields = ('name', )


# =========================================================================================================== #

class PublishedCoinFilter(admin.SimpleListFilter):
    title = "Used on the site or not"
    parameter_name = "has_published_coin"

    def lookups(self, request, model_admin):
        return [
            ("yes", "Used chains"),
            ("no", "Not used chains"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(coin__is_published=True).distinct()
        if self.value() == "no":
            return queryset.exclude(coin__is_published=True).distinct()
        return queryset


@admin.register(Chain)
class ChainAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_image', 'name', 'has_published_coin', )
    list_display_links = ('id', 'name', 'has_published_coin', )

    readonly_fields = ('slug', )
    formfield_overrides = {
        models.ImageField: {'widget': ImageFileInput},
    }

    search_fields = ('name', )
    autocomplete_fields = ('explorer', )
    list_filter = (PublishedCoinFilter, )

    def has_published_coin(self, obj):
        """ Отображает ✅ если у Chain есть опубликованные монеты, иначе ❌ """
        has_coin = obj.coin.filter(is_published=True).exists()
        icon = "✅" if has_coin else "❌"
        return format_html(f"<b>{icon}</b>")

    has_published_coin.short_description = "Active on website"
    has_published_coin.admin_order_field = "contract_address__coin__is_published"

    def display_image(self, obj):
        if hasattr(obj, 'image'):
            img_url = obj.image.url if obj.image else None
            if img_url:
                return mark_safe(f'<img src="{img_url}" style="width: 60px; height: 60px;" />')
        return "No Image"
    display_image.short_description = 'Image'
