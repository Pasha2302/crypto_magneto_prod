from django.contrib import admin
from django.utils.html import format_html
from app.db_models.db_secondary import Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    # form = CountryAdminForm

    list_display = ('id', 'name', 'emoji_flag_display', 'code_alpha_2', 'code_alpha_3', )
    list_display_links = ('id', 'name')
    readonly_fields = ('id', )
    search_fields = ('name', 'code_alpha_2', 'code_alpha_3')
    ordering = ('id',)

    def emoji_flag_display(self, obj):
        """ Отображает эмодзи флаг страны или ❌, если флаг не задан """
        icon = obj.emoji_flag or "❌"
        return format_html(f"<b>{icon}</b>")

    emoji_flag_display.short_description = "Flag"
    emoji_flag_display.admin_order_field = "emoji_flag"




