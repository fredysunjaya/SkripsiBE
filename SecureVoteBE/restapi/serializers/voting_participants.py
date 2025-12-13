from django.db.models.expressions import fields
from rest_framework import serializers
from SecureVoteBE.restapi.models.voting_participants import VotingParticipant
from SecureVoteBE.restapi.models.users import User
from SecureVoteBE.restapi.models.votings import Voting

class VotingParticipantSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    voting = serializers.PrimaryKeyRelatedField(queryset=Voting.objects.all())
    
    class Meta:
        model = VotingParticipant
        fields = "__all__"
        depth = 1