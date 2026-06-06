from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response
from skripsiBE.app.models.user_logs import UserLog
from skripsiBE.app.serializers.user_logs import UserLogSerializer
from rest_framework.settings import api_settings
from skripsiBE.app.custom_basic_authentication import EmailAuthentication
from skripsiBE.app.custom_session_authentication import CookieSessionAuthentication
from skripsiBE.app.custom_is_authenticated import (
    IsAuthenticatedUser,
    IsAdminUser,
    IsSupervisorUser,
)
from django.utils import timezone
from django.db.models import Count
from django.db.models import Q
from datetime import datetime, time
from zoneinfo import ZoneInfo


class UserLogsList(APIView):
    authentication_classes = [CookieSessionAuthentication, EmailAuthentication]
    permission_classes = [IsAuthenticatedUser]

    def get(self, request, group, user):
        user_logs = []

        # dashboard
        if request.query_params.get("stats") is not None:
            user_logs = (
                UserLog.objects.filter(user=user, group=group)
                .values("type")
                .annotate(count=Count("id"))
                .order_by("type")
            )

            result_dict = dict((item["type"], item["count"]) for item in user_logs)

            return Response(result_dict)

        # attendance history
        else:
            user_logs = (
                UserLog.objects.filter(user=user, group=group)
                .select_related("user", "group", "attendance_type")
                .order_by("-start_date_time")
            )

            # get today log
            wib = ZoneInfo("Asia/Jakarta")

            today_wib = timezone.localdate()

            start_wib = datetime.combine(today_wib, time.min).replace(tzinfo=wib)
            end_wib = datetime.combine(today_wib, time.max).replace(tzinfo=wib)

            start_utc = start_wib.astimezone(ZoneInfo("UTC"))
            end_utc = end_wib.astimezone(ZoneInfo("UTC"))

            today_log = (
                UserLog.objects.filter(
                    user=user,
                    group=group,
                )
                .filter(
                    Q(start_date_time__range=(start_utc, end_utc))
                    | Q(end_date_time__range=(start_utc, end_utc))
                )
                .first()
            )

        paginator = api_settings.DEFAULT_PAGINATION_CLASS()
        result_page = paginator.paginate_queryset(user_logs, request)

        serializers = UserLogSerializer(result_page, many=True)
        serializers2 = UserLogSerializer(today_log)

        response = paginator.get_paginated_response(serializers.data)
        response.data["today_log"] = serializers2.data
        return response

    def post(self, request):
        serializer = UserLogSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogDetails(APIView):
    authentication_classes = [CookieSessionAuthentication | EmailAuthentication]
    permission_classes = [IsAuthenticatedUser]

    def get_user_log(self, id):
        user_log = get_object_or_404(UserLog, pk=id)
        return user_log

    def get(self, request, id):
        serializer = UserLogSerializer(self.get_user_log(id))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        serializer = UserLogSerializer(
            self.get_user_log(id), data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        user_log = self.get_user_log(id)
        user_log.delete()
        return Response("UserLog Deleted", status=status.HTTP_204_NO_CONTENT)
