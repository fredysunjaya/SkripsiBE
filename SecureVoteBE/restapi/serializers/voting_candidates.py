from rest_framework import serializers
from SecureVoteBE.restapi.models.voting_candidates import VotingCandidate

class VotingCandidate(serializers.ModelSerializer):
    class Meta:
        model = VotingCandidate
        fields = "__all__"