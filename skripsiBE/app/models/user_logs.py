from django.db import models
from .users import User
from .groups import Group
from .attendance_types import AttendanceType


class UserLog(models.Model):
    types = {
        "late": "Late",
        "leave": "Leave",
        "override clock in": "Override Clock In",
        "override clock out": "Override Clock Out",
        "override clock in and out": "Override Clock In and Out",
    }

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    attendance_type = models.ForeignKey(
        AttendanceType, on_delete=models.CASCADE, null=True
    )
    start_date_time = models.DateTimeField(null=True)
    end_date_time = models.DateTimeField(null=True)
    type = models.CharField(max_length=255, choices=types, null=True)
    reason = models.TextField(null=True)

    class Meta:
        db_table = "user_logs"
        indexes = [
            models.Index(fields=["user", "group", "attendance_type"]),
        ]
