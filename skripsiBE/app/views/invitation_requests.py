from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from skripsiBE.app.models.invitation_requests import InvitationRequest
from skripsiBE.app.serializers.invitation_requests import InvitationRequestSerializer

@api_view(["GET", "POST"])
def InvitationRequestsList(request):
  if request.method == "GET":
    users = InvitationRequest.objects.all()
    serializers = InvitationRequestSerializer(users, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)
  
  if request.method == "POST":
    serializer = InvitationRequestSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
      
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
def InvitationRequestDetails(request, id):
  try:
    user = InvitationRequest.objects.get(pk=id)
  except InvitationRequest.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  except:
    return Response(status=status.HTTP_400_BAD_REQUEST);
  
  if request.method == "GET":
    serializer = InvitationRequestSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  if request.method == "PUT":
    serializer = InvitationRequestSerializer(user, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
      
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  if request.method == "DELETE":
    user.delete()
    return Response("InvitationRequest Deleted", status=status.HTTP_204_NO_CONTENT)
    