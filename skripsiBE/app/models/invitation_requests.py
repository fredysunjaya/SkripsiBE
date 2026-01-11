from django.db import models
from .groups import Group
from .users import User

class InvitationRequest(models.Model):
    status = {
        "pending": "Pending",
        "accepted": "Accepted",
        "rejected": "Rejected",
        "cancelled ": "Cancelled"
    }

    invitee = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="invitee_set")
    inviter = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="inviter_set")
    group = models.ForeignKey(Group, on_delete=models.RESTRICT)
    status = models.CharField(max_length=255, choices=status)
    
    class Meta:
        db_table = "invitation_requests"