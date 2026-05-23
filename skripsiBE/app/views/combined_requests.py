from rest_framework.decorators import APIView
from rest_framework.response import Response
from skripsiBE.app.models.leave_requests import LeaveRequest
from skripsiBE.app.models.override_requests import OverrideRequest
from skripsiBE.app.serializers.leave_requests import LeaveRequestSerializer
from skripsiBE.app.serializers.override_requests import OverrideRequestSerializer
from rest_framework.settings import api_settings
from skripsiBE.app.custom_basic_authentication import EmailAuthentication
from skripsiBE.app.custom_session_authentication import CookieSessionAuthentication
from skripsiBE.app.custom_is_authenticated import (
    IsAuthenticatedUser,
    IsAdminUser,
    IsSupervisorUser,
)


class CombinedRequests(APIView):
    authentication_classes = [CookieSessionAuthentication, EmailAuthentication]
    permission_classes = [IsSupervisorUser]

    def get(self, request, user, group):
        is_requested = request.query_params.get("isRequested")
        is_requested_spv = request.query_params.get("isRequestedSpv")

        # my team request
        if is_requested_spv is not None:
            print(user, group)
            override_qs = OverrideRequest.objects.filter(
                supervisor=user, group=group, status__in=["requested"]
            ).select_related("user", "supervisor", "group")

            leave_qs = LeaveRequest.objects.filter(
                supervisor=user, group=group, status__in=["requested"]
            ).select_related("user", "supervisor", "group", "attendance_type")

            override_data = OverrideRequestSerializer(override_qs, many=True).data
            leave_data = LeaveRequestSerializer(leave_qs, many=True).data

            # Add a type field (important!)
            for item in override_data:
                item["type"] = "override"

            for item in leave_data:
                item["type"] = "leave"

            combined = override_data + leave_data

            # Sort (VERY IMPORTANT — use a common field)
            combined.sort(key=lambda x: x["created_at"], reverse=True)

            # Paginate AFTER merging
            paginator = api_settings.DEFAULT_PAGINATION_CLASS()
            page = paginator.paginate_queryset(combined, request)

            return paginator.get_paginated_response(page)

        # requested member details
        elif is_requested == "true":
            override_qs = OverrideRequest.objects.filter(
                user=user, group=group, status__in=["requested"]
            ).select_related("user", "supervisor", "group")

            leave_qs = LeaveRequest.objects.filter(
                user=user, group=group, status__in=["requested"]
            ).select_related("user", "supervisor", "group", "attendance_type")

            override_data = OverrideRequestSerializer(override_qs, many=True).data
            leave_data = LeaveRequestSerializer(leave_qs, many=True).data

            # Add a type field (important!)
            for item in override_data:
                item["type"] = "override"

            for item in leave_data:
                item["type"] = "leave"

            combined = override_data + leave_data
            # Sort (VERY IMPORTANT — use a common field)
            combined.sort(key=lambda x: x["created_at"], reverse=True)

            # Paginate AFTER merging
            paginator = api_settings.DEFAULT_PAGINATION_CLASS()
            page = paginator.paginate_queryset(combined, request)

            return paginator.get_paginated_response(page)

        # history member details
        if is_requested == "false":
            override_qs2 = OverrideRequest.objects.filter(
                user=user, group=group, status__in=["approved", "rejected", "cancelled"]
            ).select_related("user", "supervisor", "group")

            leave_qs2 = LeaveRequest.objects.filter(
                user=user, group=group, status__in=["approved", "rejected", "cancelled"]
            ).select_related("user", "supervisor", "group", "attendance_type")

            override_data2 = OverrideRequestSerializer(override_qs2, many=True).data
            leave_data2 = LeaveRequestSerializer(leave_qs2, many=True).data

            for item in override_data2:
                item["type"] = "override"

            for item in leave_data2:
                item["type"] = "leave"

            combined2 = override_data2 + leave_data2
            combined2.sort(key=lambda x: x["created_at"], reverse=True)

            paginator2 = api_settings.DEFAULT_PAGINATION_CLASS()
            page2 = paginator2.paginate_queryset(combined2, request)

            return paginator2.get_paginated_response(page2)
