from rest_framework import serializers
from skripsiBE.app.models.groups import VotingChoice
from skripsiBE.app.models.users import User
from skripsiBE.app.models.roles import Voting

class VotingChoiceSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    voting = serializers.PrimaryKeyRelatedField(queryset=Voting.objects.all())
    candidate = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    class Meta:
        model = VotingChoice
        fields = "__all__"
        depth = 1