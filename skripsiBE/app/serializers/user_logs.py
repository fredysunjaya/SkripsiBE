from rest_framework import serializers
from skripsiBE.app.models.user_logs import UserLog
from skripsiBE.app.models.users import User
from skripsiBE.app.models.groups import Group
from skripsiBE.app.models.attendance_types import AttendanceType
from skripsiBE.app.serializers.groups import GroupSerializer
from skripsiBE.app.serializers.users import UserSerializer
from skripsiBE.app.serializers.attendance_types import AttendanceTypeSerializer


class UserLogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    group = GroupSerializer(read_only=True)
    attendance_type = AttendanceTypeSerializer(read_only=True)

    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="user", write_only=True
    )
    group_id = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), source="group", write_only=True
    )
    attendance_type_id = serializers.PrimaryKeyRelatedField(
        queryset=AttendanceType.objects.all(), source="attendance_type", write_only=True
    )

    class Meta:
        model = UserLog
        fields = "__all__"
