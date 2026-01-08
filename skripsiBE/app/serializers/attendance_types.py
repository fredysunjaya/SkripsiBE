from rest_framework import serializers
from skripsiBE.app.models.attendance_types import AttendanceType
from skripsiBE.app.models.groups import Group

class AttendanceTypeSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
    
    class Meta:
        model = AttendanceType
        depth = 1
        fields = "__all__"