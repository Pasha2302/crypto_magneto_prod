from django.contrib import admin
from app.db_models import AuditStatus, AuditProvider


@admin.register(AuditStatus)
class AuditStatusAdmin(admin.ModelAdmin):
    pass


@admin.register(AuditProvider)
class AuditProviderAdmin(admin.ModelAdmin):
    pass
