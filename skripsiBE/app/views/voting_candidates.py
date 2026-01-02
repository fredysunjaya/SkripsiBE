from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from skripsiBE.app.models.work_types import VotingCandidate
from skripsiBE.app.serializers.voting_candidates import VotingCandidateSerializer

@api_view(["GET", "POST"])
def voting_candidates_list(request):
  if request.method == "GET":
    candidates = VotingCandidate.objects.all()
    serializers = VotingCandidateSerializer(candidates, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)

  if request.method == "POST":
    print(request.data)
    serializer = VotingCandidateSerializer(data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
def voting_candidate_details(request):
  try:
    candidate = VotingCandidate.objects.get(pk=id)
  except VotingCandidate.DoesNotExist():
    return Response(candidate, status=status.HTTP_404_NOT_FOUND)
  except:
    return Response(status=status.HTTP_400_BAD_REQUEST)

  if request.method == "GET":
    serializer = VotingCandidateSerializer(candidate)

    return Response(serializer.data, status=status.HTTP_200_OK)

  if request.method == "PUT":
    serializer = VotingCandidateSerializer(candidate, data=request.data)

    if serializer.is_valid():
      serializer.save()

      return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  if request.method == "DELETE":
    candidate.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)