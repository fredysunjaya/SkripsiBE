from rest_framework import serializers
from SecureVoteBE.restapi.models.voting_choices import VotingChoice

class VotingChoice(serializers.ModelSerializer):
    class Meta:
        model = VotingChoice
        fields = "__all__"