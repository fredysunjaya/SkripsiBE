from rest_framework import serializers
from SecureVoteBE.restapi.models.voting_choices import VotingChoice
from SecureVoteBE.restapi.models.users import User
from SecureVoteBE.restapi.models.votings import Voting

class VotingChoiceSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    voting = serializers.PrimaryKeyRelatedField(queryset=Voting.objects.all())
    candidate = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    class Meta:
        model = VotingChoice
        fields = "__all__"
        depth = 1