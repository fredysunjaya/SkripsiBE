from django.db import models
from .users import User
from .groups import Group
from .attendance_types import AttendanceType
from .users import User


class LeaveRequest(models.Model):
    status = {
        "pending": "Pending",
        "accepted": "Accepted",
        "rejected": "Rejected",
        "cancelled ": "Cancelled",
    }

    user = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name="user_leave_set"
    )
    group = models.ForeignKey(Group, on_delete=models.RESTRICT)
    supervisor = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name="supervisor_leave_set"
    )
    attendance_type = models.ForeignKey(AttendanceType, on_delete=models.RESTRICT)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    status = models.CharField(max_length=255, choices=status)
    reason = models.TextField()

    class Meta:
        db_table = "leave_requests"
