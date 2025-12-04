from django.db import models


class DBConnectionSnapshot(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    active_connections = models.IntegerField()
    idle_connections = models.IntegerField()
    idle_in_transaction = models.IntegerField()

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "DB Connection Snapshot"
        verbose_name_plural = "DB Connection Snapshots"

    def __str__(self):
        return f"{self.timestamp} — active: {self.active_connections}, idle: {self.idle_connections}"
