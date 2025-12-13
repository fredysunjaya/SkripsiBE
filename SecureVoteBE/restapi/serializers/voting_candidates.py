from rest_framework import serializers
from SecureVoteBE.restapi.models.voting_candidates import VotingCandidate
from SecureVoteBE.restapi.models.users import User
from SecureVoteBE.restapi.models.votings import Voting


class VotingCandidateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    voting = serializers.PrimaryKeyRelatedField(queryset=Voting.objects.all())
    
    class Meta:
        model = VotingCandidate
        fields = "__all__"
        depth = 1