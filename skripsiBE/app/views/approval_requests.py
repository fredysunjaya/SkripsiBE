from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response
from skripsiBE.app.models.approval_requests import ApprovalRequest
from skripsiBE.app.serializers.approval_requests import ApprovalRequestSerializer
from rest_framework.settings import api_settings
from skripsiBE.app.custom_basic_authentication import EmailAuthentication
from skripsiBE.app.custom_session_authentication import CookieSessionAuthentication
from skripsiBE.app.custom_is_authenticated import IsAuthenticatedUser, IsAdminUser, IsSupervisorUser

class GetUserApprovalRequestsForUser(APIView):
  def get(self, request, user):
    approval_requests = ApprovalRequest.objects.filter(user=user)

    paginator = api_settings.DEFAULT_PAGINATION_CLASS()
    result_page = paginator.paginate_queryset(approval_requests, request)

    serializers = ApprovalRequestSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializers.data)
  
  def post(self, request):
    serializer = ApprovalRequestSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
class GetUserApprovalRequestsForSupervisor(APIView):
  def get(self, request, user):
    approval_requests = ApprovalRequest.objects.filter(supervisor=user)

    paginator = api_settings.DEFAULT_PAGINATION_CLASS()
    result_page = paginator.paginate_queryset(approval_requests, request)

    serializers = ApprovalRequestSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializers.data)

class ApprovalRequestDetails(APIView):
  authentication_classes = [CookieSessionAuthentication, EmailAuthentication]

  def get_approval_request(id):
    approval_request = get_object_or_404(ApprovalRequest, pk=id)
    return approval_request

  def get(self, request, id):
    self.permission_classes = [IsAuthenticatedUser]
    serializer = ApprovalRequestSerializer(self.get_approval_request(id))
    return Response(serializer.data, status=status.HTTP_200_OK)

  def put(self, request, id):
    self.permission_classes = [IsSupervisorUser]
    serializer = ApprovalRequestSerializer(self.get_approval_request(id), data=request.data)
    
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, id):
    # maybe unused
    self.permission_classes = [IsAuthenticatedUser]
    approval_request = self.get_approval_request(id)
    approval_request.delete()
    return Response("ApprovalRequest Deleted", status=status.HTTP_204_NO_CONTENT)