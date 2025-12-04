from django.contrib import admin
from django.db import models

from app.admin_registration.admin_forms.widgets.image_file_input import ImageFileInput
from app.db_models import CoinSocial, SafetyAndAudit


# class ContractAddressInline(admin.TabularInline):
#     model = ContractAddress
#     extra = 1
#     fk_name = 'coin'  # Указываем, к какой ForeignKey привязана Inline-модель
#     # readonly_fields = ('basic', )
#
#     can_delete = True
#     fields = ('address', 'chain', 'basic', )
#     autocomplete_fields = ('chain', )


class CoinSocialInline(admin.StackedInline):
    model = CoinSocial

    formfield_overrides = {
        models.ImageField: {'widget': ImageFileInput},
    }
    extra = 1

    # fieldsets = (
    #     (None, {
    #         'fields': ('image', 'scheme', )
    #     }),
    # )

class SafetyAndAuditInline(admin.StackedInline):
    model = SafetyAndAudit
