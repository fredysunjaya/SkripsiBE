from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response
from skripsiBE.app.models.user_logs import UserLog
from skripsiBE.app.serializers.user_logs import UserLog
from rest_framework.settings import api_settings 
from skripsiBE.app.custom_basic_authentication import EmailAuthentication
from skripsiBE.app.custom_session_authentication import CookieSessionAuthentication
from skripsiBE.app.custom_is_authenticated import IsAuthenticatedUser, IsAdminUser, IsSupervisorUser

class UserLogsList(APIView):
  authentication_classes = [CookieSessionAuthentication, EmailAuthentication]
  permission_classes = [IsAuthenticatedUser]

  def get(self, request, group, user):
    user_logs = UserLog.objects.filter(group=group, user=user)

    paginator = api_settings.DEFAULT_PAGINATION_CLASS()
    result_page = paginator.paginate_queryset(user_logs, request)

    serializers = UserLog(result_page, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)

  def post(self, request):
    serializer = UserLog(data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogDetails(APIView):
  authentication_classes = [CookieSessionAuthentication | EmailAuthentication]
  permission_classes = [IsAuthenticatedUser]
  
  def get_user_log(id):
    user_log = get_object_or_404(UserLog, pk=id)
    return user_log

  def get(self, request, id):
    serializer = UserLog(self.get_user_log(id))
    return Response(serializer.data, status=status.HTTP_200_OK)

  def put(self, request, id):
    serializer = UserLog(self.get_user_log(id), data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, id):
    # maybe unused
    user_log = self.get_user_log(id)
    user_log.delete()
    return Response("UserLog Deleted", status=status.HTTP_204_NO_CONTENT)