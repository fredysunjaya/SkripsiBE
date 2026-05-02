from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response
from skripsiBE.app.models.attendance_types import AttendanceType
from skripsiBE.app.serializers.attendance_types import AttendanceTypeSerializer
from rest_framework.settings import api_settings
from skripsiBE.app.custom_basic_authentication import EmailAuthentication
from skripsiBE.app.custom_session_authentication import CookieSessionAuthentication
from skripsiBE.app.custom_is_authenticated import (
    IsAuthenticatedUser,
    IsAdminUser,
    IsSupervisorUser,
)


class AttendanceTypeList(APIView):
    authentication_classes = [CookieSessionAuthentication, EmailAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, group):
        attendance_types = AttendanceType.objects.filter(group=group)

        paginator = api_settings.DEFAULT_PAGINATION_CLASS()
        result_page = paginator.paginate_queryset(attendance_types, request)

        serializers = AttendanceTypeSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializers.data)

    def post(self, request):
        serializer = AttendanceTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttendanceTypeDetails(APIView):
    authentication_classes = [CookieSessionAuthentication, EmailAuthentication]
    permission_classes = [IsAdminUser]

    def get_attendance_type(id):
        attendance_type = get_object_or_404(AttendanceType, pk=id)
        return attendance_type

    def get(self, request, id):
        serializer = AttendanceTypeSerializer(self.get_attendance_type(id))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        serializer = AttendanceTypeSerializer(
            self.get_attendance_type(id), data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        attendance_type = self.get_attendance_type(id)
        attendance_type.delete()
        return Response("AttendanceType Deleted", status=status.HTTP_204_NO_CONTENT)
