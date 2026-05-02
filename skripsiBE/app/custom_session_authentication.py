from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from skripsiBE.app.models.users import User


class CookieSessionAuthentication(BaseAuthentication):
    def authenticate(self, request):
        user_id = request.session.get("user_id")

        if not user_id:
            return None

        try:
            user = User.objects.get(id=request.session.get("user_id"))
        except User.DoesNotExist:
            return AuthenticationFailed("Invalid session")

        return (user, None)
