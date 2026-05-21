from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response
from skripsiBE.app.models.working_hours import WorkingHours
from skripsiBE.app.serializers.working_hours import WorkingHourSerializer
from rest_framework.settings import api_settings
from skripsiBE.app.custom_basic_authentication import EmailAuthentication
from skripsiBE.app.custom_session_authentication import CookieSessionAuthentication
from skripsiBE.app.custom_is_authenticated import (
    IsAuthenticatedUser,
    IsAdminUser,
    IsSupervisorUser,
)


class WorkingHoursList(APIView):
    authentication_classes = [CookieSessionAuthentication, EmailAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, group):
        working_hours = WorkingHours.objects.filter(group=group).select_related("group")

        paginator = api_settings.DEFAULT_PAGINATION_CLASS()
        result_page = paginator.paginate_queryset(working_hours, request)

        serializers = WorkingHourSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializers.data)

    def post(self, request):
        serializer = WorkingHourSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkingHourDetails(APIView):
    authentication_classes = [CookieSessionAuthentication, EmailAuthentication]
    permission_classes = [IsAdminUser]

    def get_working_hour(self, id):
        workingHours = get_object_or_404(WorkingHours, pk=id)
        return workingHours

    def get(self, request, id):
        serializer = WorkingHourSerializer(self.get_working_hour(id))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        serializer = WorkingHourSerializer(self.get_working_hour(id), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        working_hour = self.get_working_hour(id)
        working_hour.delete()
        return Response("WorkingHours Deleted", status=status.HTTP_204_NO_CONTENT)
