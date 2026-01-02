from rest_framework import serializers
from skripsiBE.app.models.work_types import VotingCandidate
from skripsiBE.app.models.users import User
from skripsiBE.app.models.roles import Voting


class VotingCandidateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    voting = serializers.PrimaryKeyRelatedField(queryset=Voting.objects.all())
    
    class Meta:
        model = VotingCandidate
        fields = "__all__"
        depth = 1