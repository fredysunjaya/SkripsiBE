from rest_framework.permissions import BasePermission
from skripsiBE.app.models.users import User
from skripsiBE.app.models.user_groups import UserGroup


class IsAuthenticatedUser(BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, User)


class IsSupervisorUser(BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user, User):
            return UserGroup.objects.filter(
                user=request.user,
                group_id=request.query_params.get("group_id"),
                role__name="supervisor",
            ).exists()
        return False


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):

        if isinstance(request.user, User):
            return UserGroup.objects.filter(
                user=request.user,
                group_id=request.query_params.get("group_id"),
                role__name="admin",
            ).exists()
        return False
