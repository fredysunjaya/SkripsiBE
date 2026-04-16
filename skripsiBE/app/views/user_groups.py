from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response
from skripsiBE.app.models.user_groups import UserGroup
from skripsiBE.app.serializers.user_groups import UserGroupSerializer
from rest_framework.settings import api_settings
from skripsiBE.app.custom_basic_authentication import EmailAuthentication
from skripsiBE.app.custom_session_authentication import CookieSessionAuthentication
from skripsiBE.app.custom_is_authenticated import IsAuthenticatedUser, IsAdminUser, IsSupervisorUser

class UserGroupsList(APIView):
  authentication_classes = [CookieSessionAuthentication, EmailAuthentication]
  permission_classes = [IsAuthenticatedUser]

  def get(self, request, user):
    user_groups = UserGroup.objects.filter(user=user)

    paginator = api_settings.DEFAULT_PAGINATION_CLASS()
    result_page = paginator.paginate_queryset(user_groups, request)

    serializers = UserGroupSerializer(result_page, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)

class UserGroupsMembers(APIView):
  authentication_classes = [CookieSessionAuthentication, EmailAuthentication]
  permission_classes = [IsAdminUser]

  def get(self, request, group):
    user_groups = UserGroup.objects.filter(group=group)

    paginator = api_settings.DEFAULT_PAGINATION_CLASS()
    result_page = paginator.paginate_queryset(user_groups, request)

    serializers = UserGroupSerializer(result_page, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)

  def post(self, request):
    serializer = UserGroupSerializer(data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserGroupDetails(APIView):
  authentication_classes = [CookieSessionAuthentication, EmailAuthentication]
  permission_classes = [IsAdminUser]

  def get_user_group(id):
    user_group = get_object_or_404(UserGroup, pk=id)
    return user_group

  def get(self, request, id):
    serializer = UserGroupSerializer(self.get_user_group(id))
    return Response(serializer.data, status=status.HTTP_200_OK)

  def put(self, request, id):
    serializer = UserGroupSerializer(self.get_user_group(id), data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, id):
    user_group = self.get_user_group(id)
    user_group.delete()
    return Response("UserGroup Deleted", status=status.HTTP_204_NO_CONTENT)
