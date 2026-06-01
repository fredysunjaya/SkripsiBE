from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response
from skripsiBE.app.models.groups import Group
from skripsiBE.app.models.users import User
from skripsiBE.app.models.user_groups import UserGroup
from skripsiBE.app.models.working_hours import WorkingHours
from skripsiBE.app.models.attendance_types import AttendanceType
from skripsiBE.app.serializers.groups import GroupSerializer
from rest_framework.settings import api_settings
from skripsiBE.app.custom_basic_authentication import EmailAuthentication
from skripsiBE.app.custom_session_authentication import CookieSessionAuthentication
from skripsiBE.app.custom_is_authenticated import (
    IsAuthenticatedUser,
    IsAdminUser,
    IsSupervisorUser,
)
import bcrypt


class GroupsList(APIView):
    # maybe unused
    authentication_classes = [CookieSessionAuthentication, EmailAuthentication]
    permission_classes = [IsAuthenticatedUser]

    # maybe unused
    def get(self, request):
        groups = Group.objects.all()

        paginator = api_settings.DEFAULT_PAGINATION_CLASS()
        result_page = paginator.paginate_queryset(groups, request)

        serializers = GroupSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializers.data)

    def post(self, request):
        serializer = GroupSerializer(data=request.data.get("group"))
        if serializer.is_valid():
            serializer.save()

            UserGroup.objects.create(
                user_id=request.data.get("user_id"),
                group_id=serializer.data.get("id"),
                role_id=1,
            )

            days = request.data.get("working_days")
            start_time = request.data.get("working_hours").get("start_time")
            end_time = request.data.get("working_hours").get("end_time")
            for item in days:
                WorkingHours.objects.create(
                    group_id=serializer.data.get("id"),
                    day=item,
                    start_time=start_time,
                    end_time=end_time,
                )

            attendance_types = request.data.get("attendance_types")
            for item in attendance_types:
                AttendanceType.objects.create(
                    name=item.get("name"),
                    group_id=serializer.data.get("id"),
                    max_days=item.get("max_days"),
                    is_deleted=False,
                )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupDetails(APIView):
    authentication_classes = [CookieSessionAuthentication, EmailAuthentication]

    def get_group(self, id):
        group = get_object_or_404(Group, pk=id)
        return group

    def get(self, request, id):
        self.permission_classes = [IsAuthenticatedUser]

        serializer = GroupSerializer(self.get_group(id))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        self.permission_classes = [IsAdminUser]

        serializer = GroupSerializer(
            self.get_group(id), data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        user = User.objects.get(email=request.data.get("email"))

        if not bcrypt.checkpw(
            request.data.get("password").encode("utf-8"), user.password.encode("utf-8")
        ):
            return Response(
                {"error_code": 6, "error": "Invalid password"},
            )

        self.permission_classes = [IsAdminUser]
        group = self.get_group(id)

        group.delete()
        return Response("Group Deleted", status=status.HTTP_204_NO_CONTENT)
