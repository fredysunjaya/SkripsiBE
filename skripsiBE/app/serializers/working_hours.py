from rest_framework import serializers
from skripsiBE.app.models.working_hours import WorkingHours
from skripsiBE.app.models.groups import Group

class WorkingHourSerializer(serializers.ModelSerializer):
    group_id = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), source="group", write_only=True)

    class Meta:
        model = WorkingHours
        depth = 1
        fields = "__all__"