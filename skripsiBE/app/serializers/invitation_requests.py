from rest_framework import serializers
from skripsiBE.app.models.invitation_requests import InvitationRequest
from skripsiBE.app.models.groups import Group
from skripsiBE.app.models.users import User
from skripsiBE.app.serializers.users import UserSerializer
from skripsiBE.app.serializers.groups import GroupSerializer


class InvitationRequestSerializer(serializers.ModelSerializer):
    group = GroupSerializer(read_only=True)
    invitee = UserSerializer(read_only=True)
    inviter = UserSerializer(read_only=True)

    group_id = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), source="group", write_only=True
    )
    invitee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="invitee", write_only=True
    )
    inviter_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="inviter", write_only=True
    )

    class Meta:
        model = InvitationRequest
        fields = "__all__"
