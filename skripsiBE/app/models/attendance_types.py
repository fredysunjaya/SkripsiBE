from django.db import models
from .groups import Group


class AttendanceType(models.Model):
    name = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    max_days = models.IntegerField()
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "attendance_types"
        indexes = [
            models.Index(fields=["group"]),
        ]
