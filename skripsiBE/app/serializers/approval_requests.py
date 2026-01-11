from rest_framework import serializers
from skripsiBE.app.models.approval_requests import ApprovalRequest
from skripsiBE.app.models.users import User
from skripsiBE.app.models.groups import Group
from skripsiBE.app.models.attendance_types import AttendanceType

class ApprovalRequestSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
    attendance_type = serializers.PrimaryKeyRelatedField(queryset=AttendanceType.objects.all())
    
    class Meta:
        model = ApprovalRequest
        depth = 2
        fields = "__all__"