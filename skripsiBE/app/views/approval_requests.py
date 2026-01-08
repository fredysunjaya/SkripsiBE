from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from skripsiBE.app.models.approval_requests import ApprovalRequest
from skripsiBE.app.serializers.approval_requests import ApprovalRequestSerializer

@api_view(["GET", "POST"])
def users_list(request):
  if request.method == "GET":
    users = ApprovalRequest.objects.all()
    serializers = ApprovalRequestSerializer(users, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)

  if request.method == "POST":
    serializer = ApprovalRequestSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
def user_details(request, id):
  try:
    user = ApprovalRequest.objects.get(pk=id)
  except ApprovalRequest.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  except:
    return Response(status=status.HTTP_400_BAD_REQUEST);

  if request.method == "GET":
    serializer = ApprovalRequestSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

  if request.method == "PUT":
    serializer = ApprovalRequestSerializer(user, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  if request.method == "DELETE":
    user.delete()
    return Response("ApprovalRequest Deleted", status=status.HTTP_204_NO_CONTENT)
