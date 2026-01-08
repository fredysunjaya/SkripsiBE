from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from skripsiBE.app.models.user_groups import UserGroup
from skripsiBE.app.serializers.user_groups import UserGroupSerializer

@api_view(["GET", "POST"])
def users_list(request):
  if request.method == "GET":
    users = UserGroup.objects.all()
    serializers = UserGroupSerializer(users, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)

  if request.method == "POST":
    serializer = UserGroupSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
def user_details(request, id):
  try:
    user = UserGroup.objects.get(pk=id)
  except UserGroup.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  except:
    return Response(status=status.HTTP_400_BAD_REQUEST);

  if request.method == "GET":
    serializer = UserGroupSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

  if request.method == "PUT":
    serializer = UserGroupSerializer(user, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  if request.method == "DELETE":
    user.delete()
    return Response("UserGroup Deleted", status=status.HTTP_204_NO_CONTENT)
