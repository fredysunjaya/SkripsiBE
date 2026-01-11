from rest_framework import serializers
from skripsiBE.app.models.user_logs import UserLog
from skripsiBE.app.models.users import User
from skripsiBE.app.models.groups import Group
from skripsiBE.app.models.attendance_types import AttendanceType

class UserLogSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
    attendance_type = serializers.PrimaryKeyRelatedField(queryset=AttendanceType.objects.all())

    class Meta:
        model = UserLog
        depth = 1
        fields = "__all__"