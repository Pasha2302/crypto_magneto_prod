import json
from datetime import timedelta
from django.utils.timezone import now

from django.contrib import admin
from django.db.models import Max, F, ExpressionWrapper, IntegerField
from django.db.models.functions import TruncDate
from django.urls import path
from django.shortcuts import render

from app.db_models.db_monitoring_models import DBConnectionSnapshot


@admin.register(DBConnectionSnapshot)
class DBConnectionSnapshotAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "active_connections", "idle_connections", "idle_in_transaction")
    change_list_template = "app/admin/db_connect_temp/db_monitor_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("monitor/", self.admin_site.admin_view(self.monitor_view), name="db_monitor")
        ]
        return custom_urls + urls

    def monitor_view(self, request):
        today = now().date()
        since_week = now() - timedelta(days=7)
        since_month = now() - timedelta(days=30)

        # 🔹 1) Сегодняшние данные (каждые 10 минут)
        day_qs = (
            DBConnectionSnapshot.objects
            .filter(timestamp__date=today)
            .order_by("timestamp")
            .values("timestamp", "active_connections", "idle_connections", "idle_in_transaction")
        )
        day_data = []
        for row in day_qs:
            day_data.append({
                "timestamp": row["timestamp"].isoformat(),
                "active": row["active_connections"],
                "idle": row["idle_connections"] + row["idle_in_transaction"],
            })

        # 🔹 2) Агрегаты по дням за неделю
        week_qs = (
            DBConnectionSnapshot.objects
            .filter(timestamp__gte=since_week)
            .annotate(day=TruncDate("timestamp"))
            .values("day")
            .annotate(
                active=Max("active_connections"),
                idle=Max(
                    ExpressionWrapper(F("idle_connections") + F("idle_in_transaction"), output_field=IntegerField())
                ),
            )
            .order_by("day")
        )
        week_data = []
        for row in week_qs:
            week_data.append({
                "timestamp": row["day"].isoformat(),
                "active": round(row["active"], 2) if row["active"] is not None else 0,
                "idle": round(row["idle"], 2) if row["idle"] is not None else 0,
            })

        # 🔹 3) Агрегаты по дням за месяц
        month_qs = (
            DBConnectionSnapshot.objects
            .filter(timestamp__gte=since_month)
            .annotate(day=TruncDate("timestamp"))
            .values("day")
            .annotate(
                active=Max("active_connections"),
                idle=Max(
                    ExpressionWrapper(F("idle_connections") + F("idle_in_transaction"), output_field=IntegerField())
                ),
            )
            .order_by("day")
        )
        month_data = []
        for row in month_qs:
            month_data.append({
                "timestamp": row["day"].isoformat(),
                "active": round(row["active"], 2) if row["active"] is not None else 0,
                "idle": round(row["idle"], 2) if row["idle"] is not None else 0,
            })

        context = dict(
            self.admin_site.each_context(request),
            snapshots_json=json.dumps({
                "day": day_data,
                "week": week_data,
                "month": month_data,
            }),
        )
        return render(request, "app/admin/db_connect_temp/db_monitor_page.html", context)

    def has_add_permission(self, request, obj=None):
        """
        Определяет, разрешено ли пользователю создавать новые объекты модели
        через админку Django.

        Параметры:
        ----------
        request : django.http.HttpRequest
            Объект HTTP-запроса, содержит информацию о текущем пользователе.
        obj : models.Model | None
            Экземпляр модели. Обычно None при проверке кнопки "Добавить".

        Возвращает:
        ----------
        bool
            True  — разрешить создание новых объектов (кнопка "Add" будет видна).
            False — запретить создание новых объектов (кнопка "Add" скрыта).

        Пример использования:
        --------------------
        class DBConnectionSnapshotAdmin(admin.ModelAdmin):
            list_display = ("timestamp", "active_connections", "idle_connections", "idle_in_transaction")

            def has_add_permission(self, request, obj=None):
                # Отключаем возможность добавления вручную
                return False
        """
        return False

