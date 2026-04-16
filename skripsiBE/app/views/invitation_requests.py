from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response
from skripsiBE.app.models.invitation_requests import InvitationRequest
from skripsiBE.app.serializers.invitation_requests import InvitationRequestSerializer
from rest_framework.settings import api_settings
from skripsiBE.app.custom_basic_authentication import EmailAuthentication
from skripsiBE.app.custom_session_authentication import CookieSessionAuthentication
from skripsiBE.app.custom_is_authenticated import IsAuthenticatedUser, IsAdminUser, IsSupervisorUser

class InvitationRequestsListForInvitee(APIView):
  authentication_classes = [CookieSessionAuthentication, EmailAuthentication]
  permission_classes = [IsAuthenticatedUser]

  def get(self, request, user):
    invitation_requests = InvitationRequest.objects.filter(invitee=user)

    paginator = api_settings.DEFAULT_PAGINATION_CLASS()
    result_page = paginator.paginate_queryset(invitation_requests, request)

    serializers = InvitationRequestSerializer(result_page, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)

class InvitationRequestListForInviter:
  authentication_classes = [CookieSessionAuthentication, EmailAuthentication]
  permission_classes = [IsAdminUser]

  def get(self, request, user):
    invitation_requests = InvitationRequest.objects.filter(inviter=user)

    paginator = api_settings.DEFAULT_PAGINATION_CLASS()
    result_page = paginator.paginate_queryset(invitation_requests, request)

    serializers = InvitationRequestSerializer(result_page, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)
  
  def post(self, request):
    serializer = InvitationRequestSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
      
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InvitationRequestDetails(APIView):
  authentication_classes = [CookieSessionAuthentication, EmailAuthentication]
  permission_classes = [IsAuthenticatedUser]

  def get_invitation_request(id):
    invitation_request = get_object_or_404(InvitationRequest, pk=id)
    return invitation_request
  
  def get(self, request, id):
    serializer = InvitationRequestSerializer(self.get_invitation_request(id))
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def put(self, request, id):
    serializer = InvitationRequestSerializer(self.get_invitation_request(id), data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
      
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  def delete(self, request, id):
    # maybe unused
    invitation_request = self.get_invitation_request(id)
    invitation_request.delete()
    return Response("InvitationRequest Deleted", status=status.HTTP_204_NO_CONTENT)