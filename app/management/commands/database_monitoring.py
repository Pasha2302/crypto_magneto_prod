from django.core.management.base import BaseCommand
from django.db import connection


def get_db_connections_state():
    """
    Возвращает количество соединений по состояниям: active, idle, idle in transaction
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT state, COUNT(*) 
            FROM pg_stat_activity
            WHERE datname = current_database()
            GROUP BY state;
        """)
        data = dict(cursor.fetchall())
        return {
            "active": data.get("active", 0),
            "idle": data.get("idle", 0),
            "idle_in_transaction": data.get("idle in transaction", 0)
        }


class Command(BaseCommand):
    help = "Тестовый запуск задачи test_command"

    def handle(self, *args, **options):
        data = get_db_connections_state()
        self.stdout.write(self.style.SUCCESS(
            f"\nDatabase connections state: {data['active']} / {data['idle']}")
        )
        self.stdout.write(self.style.SUCCESS(f"Задача завершена"))


# python manage.py database_monitoring
# nohup python manage.py database_monitoring > database_monitoring.log 2>&1 &
