from rest_framework import serializers
from skripsiBE.app.models.approval_requests import ApprovalRequest
from skripsiBE.app.models.users import User
from skripsiBE.app.models.groups import Group
from skripsiBE.app.models.attendance_types import AttendanceType

class ApprovalRequestSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source="user", write_only=True)
    supervisor_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source="supervisor", write_only=True)
    group_id = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), source="group", write_only=True)
    attendance_type_id = serializers.PrimaryKeyRelatedField(queryset=AttendanceType.objects.all(), source="attendance_type", write_only=True)
    
    class Meta:
        model = ApprovalRequest
        depth = 2
        fields = "__all__"