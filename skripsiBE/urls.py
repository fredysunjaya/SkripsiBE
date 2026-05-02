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
from django.urls import path
from skripsiBE.app.views import leave_requests
from skripsiBE.app.views import override_requests
from skripsiBE.app.views import attendance_types
from skripsiBE.app.views import groups
from skripsiBE.app.views import invitation_requests
from skripsiBE.app.views import roles
from skripsiBE.app.views import user_groups
from skripsiBE.app.views import user_logs
from skripsiBE.app.views import users
from skripsiBE.app.views import working_hours
from skripsiBE.app.views import leave_remaining

urlpatterns = [
    path("admin/", admin.site.urls),
    # path('leave-remaining/', leave_remaining.LeaveRemainingList.as_view()),
    path(
        "leave-remaining/<int:group>/<int:user>/",
        leave_remaining.LeaveRemainingList.as_view(),
    ),
    path("leave-remaining/<int:id>/", leave_remaining.LeaveRemainingDetails.as_view()),
    # path('leave-requests/', leave_requests.GetUserLeaveRequestsForUser.as_view()),
    path(
        "leave-requests/<int:user>/<int:group>/<str:status>/",
        leave_requests.GetUserLeaveRequestsForUser.as_view(),
    ),
    path(
        "leave-requests/<int:user>/<int:group>/",
        leave_requests.GetUserLeaveRequestsForSupervisor.as_view(),
    ),
    path(
        "leave-requests-supervisor/<int:id>/",
        leave_requests.LeaveRequestDetails.as_view(),
    ),
    # path('override-requests/', override_requests.GetUserOverrideRequestsForUser.as_view()),
    path(
        "override-requests/<int:user>/<int:group>/<str:status>/",
        override_requests.GetUserOverrideRequestsForUser.as_view(),
    ),
    path(
        "override-requests-supervisor/<int:user>/<int:group>/",
        override_requests.GetUserOverrideRequestsForSupervisor.as_view(),
    ),
    path(
        "override-requests/<int:id>/",
        override_requests.OverrideRequestDetails.as_view(),
    ),
    # path('attendance-types/', attendance_types.AttendanceTypeList.as_view()),
    path(
        "attendance-types/<int:group>/", attendance_types.AttendanceTypeList.as_view()
    ),
    path(
        "attendance-types/<int:id>/", attendance_types.AttendanceTypeDetails.as_view()
    ),
    path("groups/", groups.GroupsList.as_view()),
    path("groups/<int:id>/", groups.GroupDetails.as_view()),
    path(
        "invitation-requests-invitee/<int:user>/",
        invitation_requests.InvitationRequestsListForInvitee.as_view(),
    ),
    # path('invitation-requests-inviter/', invitation_requests.InvitationRequestListsForInviter.as_view()),
    path(
        "invitation-requests-inviter/<int:user>/",
        invitation_requests.InvitationRequestListsForInviter.as_view(),
    ),
    path(
        "invitation-requests/<int:id>/",
        invitation_requests.InvitationRequestDetails.as_view(),
    ),
    path("roles/", roles.RolesList.as_view()),
    path("roles/<int:id>/", roles.RoleDetails.as_view()),
    # path("user-groups/", user_groups.UserGroupsList.as_view()),
    path("user-groups/<int:user>/", user_groups.UserGroupsList.as_view()),
    path("user-groups-admin/<int:user>/", user_groups.UserGroupsListAdmin.as_view()),
    path("user-groups-members/<int:group>/", user_groups.UserGroupsMembers.as_view()),
    path("user-groups/<int:id>/", user_groups.UserGroupDetails.as_view()),
    # path('user-logs/', user_logs.UserLogsList.as_view()),
    path("user-logs/<int:group>/<int:user>/", user_logs.UserLogsList.as_view()),
    path("user-logs/<int:id>/", user_logs.UserLogDetails.as_view()),
    path("users/", users.UsersList.as_view()),
    path("auth/login/", users.UserLogin.as_view()),
    path("auth/logout/", users.UserLogout.as_view()),
    path("auth/register/", users.UserRegister.as_view()),
    path("auth/face-login/", users.UserFaceLogin.as_view()),
    path("users/<int:id>/", users.UserDetails.as_view()),
    # path('working-hours/', working_hours.WorkingHoursList.as_view()),
    path("working-hours/<int:group>/", working_hours.WorkingHoursList.as_view()),
    path("working-hours/<int:id>/", working_hours.WorkingHourDetails.as_view()),
]
