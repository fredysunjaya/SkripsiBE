from rest_framework import serializers
from skripsiBE.app.models.invitation_requests import InvitationRequest
from skripsiBE.app.models.groups import Group
from skripsiBE.app.models.users import User

class InvitationRequestSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
    invitee = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    inviter = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    class Meta:
        model = InvitationRequest
        depth = 1
        fields = "__all__"