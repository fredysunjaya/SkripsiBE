from django.db import models
from .users import User
from .groups import Group
from .users import User

class OverrideRequest(models.Model):
  status = { 
      "pending": "Pending",
      "accepted": "Accepted",
      "rejected": "Rejected",
      "cancelled ": "Cancelled"
    }
  
  user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="user_override_set")
  group = models.ForeignKey(Group, on_delete=models.RESTRICT)
  supervisor = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="supervisor_override_set")
  start_date_time = models.DateTimeField()
  end_date_time = models.DateTimeField()
  status = models.CharField(max_length=255, choices=status)
  reason = models.TextField()

  class Meta:
    db_table = "override_requests"