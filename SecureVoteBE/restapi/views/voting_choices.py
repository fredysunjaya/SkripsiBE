from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from SecureVoteBE.restapi.models.voting_choices import VotingChoice
from SecureVoteBE.restapi.serializers.voting_choices import VotingChoiceSerializer

@api_view(["GET", "POST"])
def voting_choices_list(request):
  if request.method == "GET":
    choices = VotingChoice.objects.all()
    serializers = VotingChoiceSerializer(choices, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)
  
  if request.method == "POST":
    serializer = VotingChoiceSerializer(data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
def voting_choice_details(request):
  try:
    choice = VotingChoice.objects.get(pk=id)
  except VotingChoice.DoesNotExist():
    return Response(choice, status=status.HTTP_404_NOT_FOUND)
  except:
    return Response(status=status.HTTP_400_BAD_REQUEST)
  
  if request.method == "GET":
    serializer = VotingChoiceSerializer(choice)

    return Response(serializer.data, status=status.HTTP_200_OK)

  if request.method == "PUT":
    serializer = VotingChoiceSerializer(choice, data=request.data)

    if serializer.is_valid():
      serializer.save()

      return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  if request.method == "DELETE":
    choice.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)