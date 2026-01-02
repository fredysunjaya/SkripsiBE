from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from skripsiBE.app.models.user_groups import VotingParticipant
from skripsiBE.app.serializers.voting_participants import VotingParticipantSerializer

@api_view(["GET", "POST"])
def voting_participants_list(request):
  if request.method == "GET":
    participants = VotingParticipant.objects.all() 
    serializers = VotingParticipantSerializer(participants, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)

  if request.method == "POST":
    serializer = VotingParticipantSerializer(data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
  
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
def voting_participant_details(request, id):
  try:
    votingParticipant = VotingParticipant.objects.get(pk=id)
  except VotingParticipant.DoesNotExist:
    return Response(f"Voting Participant {id} not Found", status=status.HTTP_404_NOT_FOUND)
  except:
    return Response(status=status.HTTP_400_BAD_REQUEST)

  if request.method == "GET":
    serializer = VotingParticipantSerializer(votingParticipant)
    
    return Response(serializer.data, status=status.HTTP_200_OK)

  if request.method == "PUT":
    serializer =  VotingParticipantSerializer(votingPariticipant, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  if request.method == "DELETE":
    votingParticipant.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)