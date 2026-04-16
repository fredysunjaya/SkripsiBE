import bcrypt
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from skripsiBE.app.models.users import User
import base64

class EmailAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        
        if not auth_header or not auth_header.startswith("Basic "):
            return None
        
        decoded = base64.b64decode(auth_header[6:]).decode("utf-8")
        email, password = decoded.split(":", 1)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("Invalid email or password")

        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            raise exceptions.AuthenticationFailed("Invalid email or password")
        
        return (user, None)