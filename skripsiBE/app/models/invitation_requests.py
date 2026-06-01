from django.utils import timezone
from django.db import models
from .groups import Group
from .users import User


class InvitationRequest(models.Model):
    status = {
        "requested": "Requested",
        "approved": "Approved",
        "rejected": "Rejected",
        "cancelled": "Cancelled",
    }

    invitee = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="invitee_set"
    )
    inviter = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="inviter_set"
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=status)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "invitation_requests"
        indexes = [
            models.Index(fields=["invitee", "inviter", "group"]),
        ]
