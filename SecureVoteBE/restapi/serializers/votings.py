from rest_framework import serializers
from SecureVoteBE.restapi.models.votings import Voting

class VotingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voting
        fields = "__all__"