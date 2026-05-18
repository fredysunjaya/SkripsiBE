from rest_framework import serializers
from skripsiBE.app.models.override_requests import OverrideRequest
from skripsiBE.app.models.users import User
from skripsiBE.app.models.groups import Group
from skripsiBE.app.serializers.users import UserSerializer
from skripsiBE.app.serializers.groups import GroupSerializer
from skripsiBE.app.serializers.attendance_types import AttendanceTypeSerializer


class OverrideRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    supervisor = UserSerializer(read_only=True)
    group = GroupSerializer(read_only=True)
    attendance_type = AttendanceTypeSerializer(read_only=True)

    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="user", write_only=True
    )
    supervisor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="supervisor", write_only=True
    )
    group_id = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), source="group", write_only=True
    )

    class Meta:
        model = OverrideRequest
        fields = "__all__"
