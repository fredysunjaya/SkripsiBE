from django.db import models
from .user_logs import UserLog
from .work_types import WorkType
from .attendance_types import AttendanceType
from .users import User

class ApprovalRequest(models.Model):
  status = {
    "requested": "Requested",
    "approved": "Approved",
    "rejected": "Rejected"
  }
  
  userLog = models.ForeignKey(UserLog, on_delete=models.RESTRICT)
  workType = models.ForeignKey(WorkType, on_delete=models.RESTRICT)
  attendanceType = models.ForeignKey(AttendanceType, on_delete=models.RESTRICT)
  supervisor = models.ForeignKey(User, on_delete=models.RESTRICT)
  start_time = models.DateTimeField()
  end_time = models.DateTimeField()
  status = models.CharField(max_length=255, choices=status)
  reason = models.TextField()

  class Meta:
    db_table = "approval_requests"