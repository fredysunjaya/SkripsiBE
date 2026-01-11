from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from skripsiBE.app.models.working_hours import WorkingHours
from skripsiBE.app.serializers.working_hours import WorkingHourSerializer

@api_view(["GET", "POST"])
def WorkingHoursList(request):
  if request.method == "GET":
    users = WorkingHours.objects.all()
    serializers = WorkingHourSerializer(users, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)

  if request.method == "POST":
    serializer = WorkingHourSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
def WorkingHourDetails(request, id):
  try:
    user = WorkingHours.objects.get(pk=id)
  except WorkingHours.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  except:
    return Response(status=status.HTTP_400_BAD_REQUEST);

  if request.method == "GET":
    serializer = WorkingHourSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

  if request.method == "PUT":
    serializer = WorkingHourSerializer(user, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  if request.method == "DELETE":
    user.delete()
    return Response("WorkingHours Deleted", status=status.HTTP_204_NO_CONTENT)
