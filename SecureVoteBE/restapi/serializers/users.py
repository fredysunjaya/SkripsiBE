from rest_framework import serializers
from SecureVoteBE.restapi.models.users import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"