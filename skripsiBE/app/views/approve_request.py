from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response
from skripsiBE.app.models.override_requests import OverrideRequest
from skripsiBE.app.models.leave_requests import LeaveRequest
from skripsiBE.app.models.invitation_requests import InvitationRequest
from skripsiBE.app.models.leave_remaining import LeaveRemaining
from skripsiBE.app.models.user_groups import UserGroup
from skripsiBE.app.serializers.override_requests import OverrideRequestSerializer
from skripsiBE.app.serializers.leave_requests import LeaveRequestSerializer
from skripsiBE.app.serializers.invitation_requests import InvitationRequestSerializer
from skripsiBE.app.models.user_logs import UserLog
from skripsiBE.app.custom_basic_authentication import EmailAuthentication
from skripsiBE.app.custom_session_authentication import CookieSessionAuthentication
from django.db.models import Q
from skripsiBE.app.custom_is_authenticated import (
    IsAuthenticatedUser,
    IsAdminUser,
    IsSupervisorUser,
)
from rest_framework.exceptions import PermissionDenied
from django.utils.dateparse import parse_datetime
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo
from django.utils import timezone


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
        start_date_time = (
            None
            if request.data.get("start_date_time") is None
            else parse_datetime(request.data.get("start_date_time"))
        )
        end_date_time = (
            None
            if request.data.get("end_date_time") is None
            else parse_datetime(request.data.get("end_date_time"))
        )
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

            user_log = (
                UserLog.objects.filter(
                    user_id=user_id,
                    group_id=group_id,
                )
                .filter(
                    Q(start_date_time__date=start_date_time)
                    | Q(end_date_time__date=end_date_time)
                )
                .first()
            )

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
                user_log.reason = reason

                if user_log.type != type:
                    user_log.type = "override clock in and out"

                user_log.save()

            return Response(status=200)
        elif request.data["type"] == "leave":
            wib = ZoneInfo("Asia/Jakarta")

            today_wib = timezone.localdate()

            start_wib = datetime.combine(today_wib, time.min).replace(tzinfo=wib)
            end_wib = datetime.combine(today_wib, time.max).replace(tzinfo=wib)

            start_utc = start_wib.astimezone(ZoneInfo("UTC")).year
            end_utc = end_wib.astimezone(ZoneInfo("UTC")).year

            attendance_type_id = request.data.get("attendance_type_id")

            leave_remaining = LeaveRemaining.objects.filter(
                user_id=user_id,
                group_id=group_id,
                attendance_type_id=attendance_type_id,
                year__range=(start_utc, end_utc),
            ).first()

            totalDays = (end_date_time.date() - start_date_time.date()).days + 1

            if leave_remaining.remaining_days - totalDays < 0:
                return Response(
                    {"error": "No remaining days available", "error_code": 1},
                )
            else:
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

                leave_remaining.remaining_days -= totalDays
                leave_remaining.save()

                for i in range(totalDays):
                    leaveDate = start_date_time + timedelta(days=i)

                    user_log = (
                        UserLog.objects.filter(
                            user_id=user_id,
                            group_id=group_id,
                        )
                        .filter(
                            Q(start_date_time__date=leaveDate)
                            | Q(end_date_time__date=leaveDate)
                        )
                        .select_related("attendance_type")
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
            # change request to approved
            invitation_request = InvitationRequest.objects.get(pk=id)
            serializer = InvitationRequestSerializer(
                invitation_request,
                data={
                    "status": status,
                },
                partial=True,
            )
            if serializer.is_valid():
                serializer.save()

            user_group = UserGroup.objects.create(
                user_id=user_id,
                group_id=group_id,
                role_id=3,
            )

            return Response(status=200)
