from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response
from skripsiBE.app.models.roles import Role
from skripsiBE.app.serializers.roles import RoleSerializer
from rest_framework.settings import api_settings
from skripsiBE.app.custom_basic_authentication import EmailAuthentication
from skripsiBE.app.custom_session_authentication import CookieSessionAuthentication
from skripsiBE.app.custom_is_authenticated import (
    IsAuthenticatedUser,
    IsAdminUser,
    IsSupervisorUser,
)


class RolesList(APIView):
    # maybe unused
    authentication_classes = [CookieSessionAuthentication, EmailAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        roles = Role.objects.all()

        paginator = api_settings.DEFAULT_PAGINATION_CLASS()
        result_page = paginator.paginate_queryset(roles, request)

        serializers = RoleSerializer(result_page, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class RoleDetails(APIView):
    # maybe unused
    authentication_classes = [CookieSessionAuthentication, EmailAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, id):
        role = get_object_or_404(Role, pk=id)

        serializer = RoleSerializer(role)
        return Response(serializer.data, status=status.HTTP_200_OK)
