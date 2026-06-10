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

    def get(self, request, group):
        self.permission_classes = [IsAuthenticatedUser]
        working_hours = WorkingHours.objects.filter(group=group).select_related("group")

        serializers = WorkingHourSerializer(working_hours, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        self.permission_classes = [IsAdminUser]
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
        workingHours = WorkingHours.objects.filter(group_id=id)
        type = request.query_params.get("type")

        if type == "working_days":
            for item in request.data.get("added_days"):
                WorkingHours.objects.create(
                    group_id=id,
                    day=item,
                    start_time=request.data.get("start_time"),
                    end_time=request.data.get("end_time"),
                )

            workingHours.filter(day__in=request.data.get("deleted_days")).delete()

            workingHours = WorkingHours.objects.filter(group_id=id)
            serializer = WorkingHourSerializer(workingHours, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        elif type == "working_hours":
            workingHours.update(
                start_time=request.data.get("start_time"),
                end_time=request.data.get("end_time"),
            )

            serializer = WorkingHourSerializer(workingHours.first())

            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        working_hour = self.get_working_hour(id)
        working_hour.delete()
        return Response("WorkingHours Deleted", status=status.HTTP_204_NO_CONTENT)
