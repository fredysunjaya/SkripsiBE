from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from skripsiBE.app.models.users import User
from skripsiBE.app.serializers.users import UserSerializer

@api_view(["GET", "POST"])
def users_list(request):
  if request.method == "GET":
    users = User.objects.all()
    serializers = UserSerializer(users, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)
  
  if request.method == "POST":
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
      
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
def user_details(request, id):
  try:
    user = User.objects.get(pk=id)
  except User.DoesNotExist:
    return Response(f"User {id} Not Found", status=status.HTTP_404_NOT_FOUND)
  except:
    return Response(status=status.HTTP_400_BAD_REQUEST);
  
  if request.method == "GET":
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  if request.method == "PUT":
    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
      
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  if request.method == "DELETE":
    user.delete()
    return Response("User Deleted", status=status.HTTP_204_NO_CONTENT)
    