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
                user_groups = UserGroup.objects.filter(user=request.user, group=request.data.get("group_id")).first()
                serializer = UserGroupSerializer(user_groups)

                return serializer.data["role"]["name"] == "supervisor"
        return None

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user, User):
                user_groups = UserGroup.objects.filter(user=request.user, group=request.data.get("group_id")).first()
                serializer = UserGroupSerializer(user_groups)

                return serializer.data["role"]["name"] == "admin"
        return None