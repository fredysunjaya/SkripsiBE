from rest_framework import serializers
from skripsiBE.app.models.user_groups import UserGroup
from skripsiBE.app.models.groups import Group
from skripsiBE.app.models.users import User
from skripsiBE.app.models.roles import Role
from skripsiBE.app.serializers.groups import GroupSerializer
from skripsiBE.app.serializers.users import UserSerializer
from skripsiBE.app.serializers.roles import RoleSerializer


class UserGroupSerializer(serializers.ModelSerializer):
    group = GroupSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    role = RoleSerializer(read_only=True)

    group_id = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), source="group", write_only=True
    )
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="user", write_only=True
    )
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), source="role", write_only=True
    )

    class Meta:
        model = UserGroup
        depth = 1
        fields = "__all__"
