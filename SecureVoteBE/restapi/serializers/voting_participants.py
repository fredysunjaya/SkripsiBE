from rest_framework import serializers
from SecureVoteBE.restapi.models.voting_participants import VotingParticipant

class VotingParticipant(serializers.ModelSerializer):
    class Meta:
        model = VotingParticipant
        fields = "__all__"