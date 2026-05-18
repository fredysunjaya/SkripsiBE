from rest_framework import serializers
from skripsiBE.app.models.groups import Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"
