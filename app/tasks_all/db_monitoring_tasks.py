from app.db_models.db_monitoring_models import DBConnectionSnapshot
from app.management.commands.database_monitoring import get_db_connections_state


def save_db_connections_snapshot():
    state = get_db_connections_state()
    DBConnectionSnapshot.objects.create(
        active_connections=state["active"],
        idle_connections=state["idle"],
        idle_in_transaction=state["idle_in_transaction"]
    )

