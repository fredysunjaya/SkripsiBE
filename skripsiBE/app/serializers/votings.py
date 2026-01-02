from rest_framework import serializers
from skripsiBE.app.models.roles import Voting

class VotingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voting
        fields = "__all__"