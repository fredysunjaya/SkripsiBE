from rest_framework import serializers
from skripsiBE.app.models.work_types import WorkType

class WorkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkType
        fields = "__all__"
        depth = 1