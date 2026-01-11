from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from skripsiBE.app.models.roles import Role
from skripsiBE.app.serializers.roles import RoleSerializer

@api_view(["GET"])
def RolesList(request):
  if request.method == "GET":
    users = Role.objects.all()
    serializers = RoleSerializer(users, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def RoleDetails(request, id):
  try:
    user = Role.objects.get(pk=id)
  except Role.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  except:
    return Response(status=status.HTTP_400_BAD_REQUEST);

  if request.method == "GET":
    serializer = RoleSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)