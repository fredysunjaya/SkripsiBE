from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response
from skripsiBE.app.models.leave_remaining import LeaveRemaining
from skripsiBE.app.serializers.leave_remaining import LeaveRemainingSerializer
from rest_framework.settings import api_settings
from skripsiBE.app.custom_basic_authentication import EmailAuthentication
from skripsiBE.app.custom_session_authentication import CookieSessionAuthentication
from skripsiBE.app.custom_is_authenticated import (
    IsAuthenticatedUser,
    IsAdminUser,
    IsSupervisorUser,
)


class LeaveRemainingList(APIView):
    authentication_classes = [CookieSessionAuthentication, EmailAuthentication]
    permission_classes = [IsAuthenticatedUser]

    def get(self, request, user, group):
        leave_remaining = LeaveRemaining.objects.filter(user=user, group=group)

        paginator = api_settings.DEFAULT_PAGINATION_CLASS()
        result_page = paginator.paginate_queryset(leave_remaining, request)

        serializers = LeaveRemainingSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializers.data)

    def post(self, request):
        serializer = LeaveRemainingSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeaveRemainingDetails(APIView):
    authentication_classes = [CookieSessionAuthentication, EmailAuthentication]
    permission_classes = [IsAuthenticatedUser]

    def get_leave_remaining(id):
        leave_remaining = get_object_or_404(LeaveRemaining, pk=id)
        return leave_remaining

    def get(self, request, id):
        serializer = LeaveRemainingSerializer(self.get_leave_remaining(id))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        serializer = LeaveRemainingSerializer(
            self.get_leave_remaining(id), data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        # maybe unused
        leave_remaining = self.get_leave_remaining(id)
        leave_remaining.delete()
        return Response("LeaveRemaining Deleted", status=status.HTTP_204_NO_CONTENT)
