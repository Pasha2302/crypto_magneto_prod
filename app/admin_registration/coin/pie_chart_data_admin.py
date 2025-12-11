from django.contrib import admin

from app.db_models import LabelPieChart


@admin.register(LabelPieChart)
class LabelPieChartAdmin(admin.ModelAdmin):
    search_fields = ('name', )

