from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response
from skripsiBE.app.models.override_requests import OverrideRequest
from skripsiBE.app.models.leave_requests import LeaveRequest
from skripsiBE.app.models.leave_remaining import LeaveRemaining
from skripsiBE.app.serializers.override_requests import OverrideRequestSerializer
from skripsiBE.app.serializers.leave_requests import LeaveRequestSerializer
from skripsiBE.app.models.user_logs import UserLog
from skripsiBE.app.custom_basic_authentication import EmailAuthentication
from skripsiBE.app.custom_session_authentication import CookieSessionAuthentication
from skripsiBE.app.custom_is_authenticated import (
    IsAuthenticatedUser,
    IsAdminUser,
    IsSupervisorUser,
)
from rest_framework.exceptions import PermissionDenied
from django.utils.dateparse import parse_datetime
from datetime import datetime, timedelta


class ApproveRequest(APIView):
    authentication_classes = [CookieSessionAuthentication, EmailAuthentication]

    def post(self, request):
        TYPE_PERMISSIONS = {
            "override": [IsSupervisorUser],
            "leave": [IsSupervisorUser],
            "invitation": [IsAuthenticatedUser],
        }
        type = request.data.get("type")
        permission_classes = TYPE_PERMISSIONS.get(type, [])

        for permission in permission_classes:
            if not permission().has_permission(request, self):
                raise PermissionDenied()

        id = request.data.get("id")
        user_id = request.data.get("user_id")
        group_id = request.data.get("group_id")
        start_date_time = request.data.get("start_date_time")
        end_date_time = request.data.get("end_date_time")
        status = request.data.get("status")
        reason = request.data.get("reason")

        if request.data["type"] == "override":
            # change request to approved
            override_request = OverrideRequest.objects.get(pk=id)
            serializer = OverrideRequestSerializer(
                override_request,
                data={
                    "status": status,
                },
                partial=True,
            )
            if serializer.is_valid():
                serializer.save()

            user_log = UserLog.objects.filter(
                start_date_time__date=parse_datetime(start_date_time).date()
            ).first()
            type = (
                "override clock in and out"
                if (end_date_time is not None and start_date_time is not None)
                else (
                    "override clock in"
                    if start_date_time is not None
                    else "override clock out"
                )
            )

            # create new user log
            if user_log is None:
                user_log = UserLog.objects.create(
                    user_id=user_id,
                    group_id=group_id,
                    attendance_type_id=None,
                    start_date_time=start_date_time,
                    end_date_time=end_date_time,
                    type=type,
                    reason=reason,
                )

            # override user log
            else:
                user_log.start_date_time = start_date_time or user_log.start_date_time
                user_log.end_date_time = end_date_time or user_log.end_date_time
                user_log.type = type
                user_log.reason = reason

                user_log.save()

            return Response(status=200)
        elif request.data["type"] == "leave":
            todayYear = datetime.now().year
            attendance_type_id = request.data.get("attendance_type_id")

            # change request to approved
            leave_request = LeaveRequest.objects.get(pk=id)
            serializer = LeaveRequestSerializer(
                leave_request,
                data={
                    "status": status,
                },
                partial=True,
            )
            if serializer.is_valid():
                serializer.save()

            leave_remaining = LeaveRemaining.objects.filter(
                user_id=user_id,
                group_id=group_id,
                attendance_type_id=attendance_type_id,
                year=todayYear,
            ).first()

            totalDays = (
                parse_datetime(end_date_time).date()
                - parse_datetime(start_date_time).date()
            ).days + 1

            if leave_remaining.remaining_days - totalDays < 0:
                return Response(
                    {"error": "No remaining days available", "error_code": 1},
                    status=400,
                )
            else:
                leave_remaining.remaining_days -= totalDays
                leave_remaining.save()

                for i in range(totalDays):
                    leaveDate = parse_datetime(start_date_time).date() + timedelta(
                        days=i
                    )

                    user_log = (
                        UserLog.objects.filter(
                            user_id=user_id,
                            group_id=group_id,
                            start_date_time__date=leaveDate,
                        )
                        .select_related("attendance_types")
                        .first()
                    )

                    # create new user log
                    if user_log is None:
                        user_log = UserLog.objects.create(
                            user_id=user_id,
                            group_id=group_id,
                            attendance_type_id=attendance_type_id,
                            start_date_time=leaveDate,
                            end_date_time=leaveDate,
                            type="leave",
                            reason=reason,
                        )

                    # update user log based on leave
                    else:
                        user_log.attendance_type_id = attendance_type_id
                        user_log.start_date_time = leaveDate
                        user_log.end_date_time = leaveDate
                        user_log.type = "leave"
                        user_log.reason = reason

                        user_log.save()

                return Response(status=200)

        elif request.data["type"] == "invitation":
            return None
