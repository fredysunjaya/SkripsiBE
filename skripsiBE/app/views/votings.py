from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from skripsiBE.app.models.roles import Voting
from skripsiBE.app.serializers.votings import VotingSerializer

@api_view(["GET", "POST"])
def votings_list(request):
  if request.method == "GET":
    votings = Voting.objects.all()
    serializers = VotingSerializer(votings, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)

  if request.method == "POST":
    serializer = VotingSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
def voting_details(request, id):
  print(request.data)
  
  try:
    voting = Voting.objects.get(pk=id)
  except Voting.DoesNotExist:
    return Response(f"Voting {id} Not Found", status=status.HTTP_404_NOT_FOUND)
  except: 
    return Response(status=status.HTTP_400_BAD_REQUEST)

  if request.method == "GET":
    serializer = VotingSerializer(voting)
    return Response(serializer.data, status=status.HTTP_200_OK)

  if request.method == "PUT":
    serializer = VotingSerializer(voting, data=request.data)
    if serializer.is_valid:
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
      
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  if request.method == "DELETE":
    voting.delete()
    return Response("Voting Deleted", status=status.HTTP_204_NO_CONTENT)