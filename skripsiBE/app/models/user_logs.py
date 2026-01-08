from django.db import models
from .users import User
from .groups import Group
from .work_types import WorkType
from .attendance_types import AttendanceType

class UserLog(models.Model):
  user = models.ForeignKey(User, on_delete=models.RESTRICT)
  group = models.ForeignKey(Group, on_delete=models.RESTRICT)
  workType = models.ForeignKey(WorkType, on_delete=models.RESTRICT)
  attendanceType = models.ForeignKey(AttendanceType, on_delete=models.RESTRICT)
  start_time = models.DateTimeField()
  end_time = models.DateTimeField()
  
  class Meta:
    db_table = "user_logs"