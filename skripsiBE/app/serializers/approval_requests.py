from rest_framework import serializers
from skripsiBE.app.models.approval_requests import ApprovalRequest
from skripsiBE.app.models.user_logs import UserLog
from skripsiBE.app.models.work_types import WorkType
from skripsiBE.app.models.attendance_types import AttendanceType

class ApprovalRequestSerializer(serializers.ModelSerializer):
    userLog = serializers.PrimaryKeyRelatedField(queryset=UserLog.objects.all())
    workType = serializers.PrimaryKeyRelatedField(queryset=WorkType.objects.all())
    attendanceType = serializers.PrimaryKeyRelatedField(queryset=attendanceType.objects.all())

    class Meta:
        model = ApprovalRequest
        depth = 2
        fields = "__all__"