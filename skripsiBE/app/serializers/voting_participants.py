from django.db.models.expressions import fields
from rest_framework import serializers
from skripsiBE.app.models.user_groups import VotingParticipant
from skripsiBE.app.models.users import User
from skripsiBE.app.models.roles import Voting

class VotingParticipantSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    voting = serializers.PrimaryKeyRelatedField(queryset=Voting.objects.all())
    
    class Meta:
        model = VotingParticipant
        fields = "__all__"
        depth = 1