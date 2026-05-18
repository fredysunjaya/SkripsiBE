from rest_framework.permissions import BasePermission
from skripsiBE.app.models.users import User
from skripsiBE.app.models.user_groups import UserGroup
from skripsiBE.app.serializers.user_groups import UserGroupSerializer


class IsAuthenticatedUser(BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, User)


class IsSupervisorUser(BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user, User):
            return request.query_params.get("role") == "supervisor"
        return None


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):

        if isinstance(request.user, User):
            return request.query_params.get("role") == "admin"
        return None
