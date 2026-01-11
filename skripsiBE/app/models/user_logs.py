from django.db import models
from .users import User
from .groups import Group
from .attendance_types import AttendanceType

class UserLog(models.Model):
  user = models.ForeignKey(User, on_delete=models.RESTRICT)
  group = models.ForeignKey(Group, on_delete=models.RESTRICT)
  attendance_type = models.ForeignKey(AttendanceType, on_delete=models.RESTRICT)
  start_date_time = models.DateTimeField()
  end_date_time = models.DateTimeField()
  
  class Meta:
    db_table = "user_logs"