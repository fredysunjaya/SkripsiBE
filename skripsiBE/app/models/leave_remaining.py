from django.db import models
from .users import User
from .groups import Group
from .attendance_types import AttendanceType

class LeaveRemaining(models.Model):
  user = models.ForeignKey(User, on_delete=models.RESTRICT)
  group = models.ForeignKey(Group, on_delete=models.RESTRICT)
  attendance_type = models.ForeignKey(AttendanceType, on_delete=models.RESTRICT)
  remaining_days = models.IntegerField()
  year = models.IntegerField()

  class Meta:
	  db_table = "leave_remaining"