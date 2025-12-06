from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe

from app.admin_registration.admin_forms.widgets.image_file_input import ImageFileInput
from app.db_models import TeamCoin


@admin.register(TeamCoin)
class TeamCoinAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_image', 'name', 'job_title',)
    list_display_links = ('name', 'job_title',)

    formfield_overrides = {
        models.ImageField: {'widget': ImageFileInput},
    }

    def display_image(self, obj):
        if hasattr(obj, 'image'):
            img_url = obj.image.url if obj.image else None
            if img_url:
                return mark_safe(f'<img src="{img_url}" style="width: 60px; height: 60px;" />')
        return "No Image"
    display_image.short_description = 'Image'

