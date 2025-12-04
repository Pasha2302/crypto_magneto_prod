from django.contrib import admin

from app.db_models.site_models.settings import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = list_display_links = ('pk', 'token', )

