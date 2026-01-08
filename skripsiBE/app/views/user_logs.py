from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from skripsiBE.app.models.user_logs import UserLog
from skripsiBE.app.serializers.user_logs import UserLog

@api_view(["GET", "POST"])
def users_list(request):
  if request.method == "GET":
    users = UserLog.objects.all()
    serializers = UserLog(users, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)

  if request.method == "POST":
    serializer = UserLog(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
def user_details(request, id):
  try:
    user = UserLog.objects.get(pk=id)
  except UserLog.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  except:
    return Response(status=status.HTTP_400_BAD_REQUEST);

  if request.method == "GET":
    serializer = UserLog(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

  if request.method == "PUT":
    serializer = UserLog(user, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  if request.method == "DELETE":
    user.delete()
    return Response("UserLog Deleted", status=status.HTTP_204_NO_CONTENT)
