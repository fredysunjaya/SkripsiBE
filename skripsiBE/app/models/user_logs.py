from django.db import models
from .users import User
from .groups import Group
from .attendance_types import AttendanceType


class UserLog(models.Model):
    types = {
        "clock_in": "Clock In",
        "clock_out": "Clock Out",
        "late": "late",
    }

    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    group = models.ForeignKey(Group, on_delete=models.RESTRICT)
    attendance_type = models.ForeignKey(AttendanceType, on_delete=models.RESTRICT)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    type = models.CharField(max_length=255, choices=types)

    class Meta:
        db_table = "user_logs"
