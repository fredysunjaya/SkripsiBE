"""
URL configuration for skripsiBE project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from skripsiBE.app.views import (
    leave_remainings,
    leave_requests,
    override_requests,
    attendance_types,
    groups,
    invitation_requests,
    roles,
    user_groups,
    user_logs,
    users,
    working_hours,
    combined_requests,
)

router = DefaultRouter()

urlpatterns = [
    path("admin/", admin.site.urls),
    # LeaveRemaining Endpoints
    path(
        "leave-remaining/<int:group>/<int:user>/",
        leave_remainings.LeaveRemainingList.as_view(),
    ),
    path(
        "leave-remaining-details/<int:id>/",
        leave_remainings.LeaveRemainingDetails.as_view(),
    ),
    # LeaveRequest Endpoints
    path(
        "leave-requests/<int:user>/<int:group>/<str:status>/",
        leave_requests.LeaveRequestsForUser.as_view(),
    ),
    path(
        "leave-requests-details/<int:id>/",
        leave_requests.LeaveRequestDetails.as_view(),
    ),
    # OverrideRequest Endpoints
    path(
        "override-requests/<int:user>/<int:group>/<str:status>/",
        override_requests.OverrideRequestsForUser.as_view(),
    ),
    path(
        "override-requests-details/<int:id>/",
        override_requests.OverrideRequestDetails.as_view(),
    ),
    # Combined Requests Endpoints
    path(
        "combined-requests/<int:user>/<int:group>/",
        combined_requests.CombinedRequests.as_view(),
    ),
    # Group endpoints
    path("groups/", groups.GroupsList.as_view()),
    path("groups-details/<int:id>/", groups.GroupDetails.as_view()),
    # AttendanceType endpoints
    path(
        "attendance-types/<int:group>/", attendance_types.AttendanceTypeList.as_view()
    ),
    path(
        "attendance-types-details/<int:id>/",
        attendance_types.AttendanceTypeDetails.as_view(),
    ),
    # InvitationRequest endpoints
    path(
        "invitation-requests/",
        invitation_requests.InvitationRequestsList.as_view(),
    ),
    path(
        "invitation-requests-details/<int:id>/",
        invitation_requests.InvitationRequestDetails.as_view(),
    ),
    # Role endpoints
    path("roles/", roles.RolesList.as_view()),
    path("roles-details/<int:id>/", roles.RoleDetails.as_view()),
    # UserGroup endpoints
    path("user-groups/", user_groups.UserGroupsList.as_view()),
    path("user-groups-details/<int:id>/", user_groups.UserGroupDetails.as_view()),
    # UserLog endpoints
    path("user-logs/<int:group>/<int:user>/", user_logs.UserLogsList.as_view()),
    path("user-logs-details/<int:id>/", user_logs.UserLogDetails.as_view()),
    # User endpoints
    path("users/", users.UsersList.as_view()),
    path("auth/login/", users.UserLogin.as_view()),
    path("auth/logout/", users.UserLogout.as_view()),
    path("auth/register/", users.UserRegister.as_view()),
    path("auth/face-login/", users.UserFaceLogin.as_view()),
    path("users-details/<int:id>/", users.UserDetails.as_view()),
    # WorkingHour endpoints
    path("working-hours/<int:group>/", working_hours.WorkingHoursList.as_view()),
    path("working-hours-details/<int:id>/", working_hours.WorkingHourDetails.as_view()),
]
