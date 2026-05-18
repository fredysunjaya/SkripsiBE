from rest_framework import serializers
from skripsiBE.app.models.working_hours import WorkingHours
from skripsiBE.app.models.groups import Group
from skripsiBE.app.serializers.groups import GroupSerializer


class WorkingHourSerializer(serializers.ModelSerializer):
    group = GroupSerializer(read_only=True)
    group_id = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), source="group", write_only=True
    )

    class Meta:
        model = WorkingHours
        fields = "__all__"
