from rest_framework import serializers
from skripsiBE.app.models.users import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["face_vector", "password"]
