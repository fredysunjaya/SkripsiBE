from rest_framework import serializers
from skripsiBE.app.models.user_groups import UserGroup
from skripsiBE.app.models.groups import Group
from skripsiBE.app.models.users import User

class UserGroupSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = UserGroup
        depth = 1
        fields = "__all__"