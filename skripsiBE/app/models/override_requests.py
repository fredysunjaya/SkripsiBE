from django.db import models
from .users import User
from .groups import Group
from .users import User
from django.utils import timezone


class OverrideRequest(models.Model):
    status = {
        "requested": "Requested",
        "approved": "Approved",
        "rejected": "Rejected",
        "cancelled": "Cancelled",
    }

    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="user_override_set"
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="supervisor_override_set"
    )
    start_date_time = models.DateTimeField(null=True)
    end_date_time = models.DateTimeField(null=True)
    status = models.CharField(max_length=255, choices=status)
    reason = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "override_requests"
        indexes = [
            models.Index(fields=["user", "group", "supervisor"]),
        ]
