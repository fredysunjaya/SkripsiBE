from rest_framework import serializers
from skripsiBE.app.models.user_groups import UserGroup
from skripsiBE.app.models.groups import Group
from skripsiBE.app.models.users import User
from skripsiBE.app.models.roles import Role

class UserGroupSerializer(serializers.ModelSerializer):
    group_id = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), source="group", write_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source="user", write_only=True)
    role_id = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), source="role", write_only=True)

    class Meta:
        model = UserGroup
        depth = 1
        fields = "__all__"