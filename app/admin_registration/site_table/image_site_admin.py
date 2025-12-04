from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe

from app.admin_registration.admin_forms.widgets.image_file_input import ImageFileInput
from app.db_models.site_models import ImageSite, ImageSocial


@admin.register(ImageSite)
class ImageSiteAdmin(admin.ModelAdmin):

    list_display = ('pk', 'display_image', 'slug', 'name', 'name_page',)
    list_display_links = ('pk', 'slug', 'name', 'name_page',)
    formfield_overrides = {
        models.ImageField: {'widget': ImageFileInput},
    }
    readonly_fields = ('pk', 'slug', )
    search_fields = ('slug', 'name', 'name_page', )

    def display_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="width: 60px; height: 60px;" />')
        return "No Image"
    display_image.short_description = 'Image'


# ----------------------------------------------------------------------------------------------------------------- #

@admin.register(ImageSocial)
class ImageSocialAdmin(admin.ModelAdmin):
    list_display = ('pk', 'display_image', 'slug', 'name', )
    list_display_links = ('pk', 'slug', 'name', )
    formfield_overrides = {
        models.ImageField: {'widget': ImageFileInput},
    }
    readonly_fields = ('pk', 'slug',)
    search_fields = ('slug', 'name', )

    def display_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="width: 60px; height: 60px;" />')
        return "No Image"
    display_image.short_description = 'Image'

