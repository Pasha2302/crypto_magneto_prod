import logfire
from django.db import connection
import time


class LogfireSQLMiddleware:
    """Логирует длительность запроса и все SQL-запросы."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(connection, 'queries'):
            connection.queries.clear()

        start = time.perf_counter()
        response = self.get_response(request)
        duration = (time.perf_counter() - start) * 1000  # ms

        logfire.info(
            "HTTP request processed",
            path=request.path,
            method=request.method,
            duration_ms=int(duration),
            total_sql=len(getattr(connection, "queries", [])),
        )

        for sql in getattr(connection, "queries", []):
            logfire.info(
                "SQL query",
                sql=sql.get("sql"),
                time=sql.get("time"),
            )

        return response
