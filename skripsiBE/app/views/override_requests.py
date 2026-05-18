from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response
from skripsiBE.app.models.override_requests import OverrideRequest
from skripsiBE.app.serializers.override_requests import OverrideRequestSerializer
from rest_framework.settings import api_settings
from skripsiBE.app.custom_basic_authentication import EmailAuthentication
from skripsiBE.app.custom_session_authentication import CookieSessionAuthentication
from skripsiBE.app.custom_is_authenticated import (
    IsAuthenticatedUser,
    IsAdminUser,
    IsSupervisorUser,
)


class OverrideRequestsForUser(APIView):
    authentication_classes = [CookieSessionAuthentication, EmailAuthentication]
    permission_classes = [IsAuthenticatedUser]

    def get(self, request, user, group, status):
        override_requests = OverrideRequest.objects.filter(
            user=user, group=group, status=status
        )

        paginator = api_settings.DEFAULT_PAGINATION_CLASS()
        result_page = paginator.paginate_queryset(override_requests, request)

        serializers = OverrideRequestSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializers.data)

    def post(self, request):
        serializer = OverrideRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OverrideRequestDetails(APIView):
    authentication_classes = [CookieSessionAuthentication, EmailAuthentication]

    def get_override_request(self, id):
        override_request = get_object_or_404(OverrideRequest, pk=id)
        return override_request

    def get(self, request, id):
        self.permission_classes = [IsAuthenticatedUser]
        serializer = OverrideRequestSerializer(self.get_override_request(id))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        self.permission_classes = [IsSupervisorUser]
        serializer = OverrideRequestSerializer(
            self.get_override_request(id), data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        self.permission_classes = [IsAuthenticatedUser]
        override_request = self.get_override_request(id)
        override_request.delete()
        return Response("OverrideRequest Deleted", status=status.HTTP_204_NO_CONTENT)
