from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response
from skripsiBE.app.models.leave_requests import LeaveRequest
from skripsiBE.app.serializers.leave_requests import LeaveRequestSerializer
from rest_framework.settings import api_settings
from skripsiBE.app.custom_basic_authentication import EmailAuthentication
from skripsiBE.app.custom_session_authentication import CookieSessionAuthentication
from skripsiBE.app.custom_is_authenticated import (
    IsAuthenticatedUser,
    IsAdminUser,
    IsSupervisorUser,
)


class GetUserLeaveRequestsForUser(APIView):
    authentication_classes = [CookieSessionAuthentication, EmailAuthentication]
    permission_classes = [IsAuthenticatedUser]

    def get(self, request, user, group, status):
        leave_requests = LeaveRequest.objects.filter(
            user=user, group=group, status=status
        )

        paginator = api_settings.DEFAULT_PAGINATION_CLASS()
        result_page = paginator.paginate_queryset(leave_requests, request)

        serializers = LeaveRequestSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializers.data)

    def post(self, request):
        serializer = LeaveRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUserLeaveRequestsForSupervisor(APIView):
    authentication_classes = [CookieSessionAuthentication, EmailAuthentication]
    permission_classes = [IsSupervisorUser]

    def get(self, request, user, group):
        leave_requests = LeaveRequest.objects.filter(
            supervisor=user, group=group, status="pending"
        )

        paginator = api_settings.DEFAULT_PAGINATION_CLASS()
        result_page = paginator.paginate_queryset(leave_requests, request)

        serializers = LeaveRequestSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializers.data)


class LeaveRequestDetails(APIView):
    authentication_classes = [CookieSessionAuthentication, EmailAuthentication]

    def get_leave_request(id):
        leave_request = get_object_or_404(LeaveRequest, pk=id)
        return leave_request

    def get(self, request, id):
        self.permission_classes = [IsAuthenticatedUser]
        serializer = LeaveRequestSerializer(self.get_leave_request(id))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        self.permission_classes = [IsSupervisorUser]
        serializer = LeaveRequestSerializer(
            self.get_leave_request(id), data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        # maybe unused
        self.permission_classes = [IsAuthenticatedUser]
        leave_request = self.get_leave_request(id)
        leave_request.delete()
        return Response("LeaveRequest Deleted", status=status.HTTP_204_NO_CONTENT)
