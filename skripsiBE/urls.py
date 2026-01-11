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
from skripsiBE.app.views import approval_requests
from skripsiBE.app.views import attendance_types
from skripsiBE.app.views import groups
from skripsiBE.app.views import invitation_requests
from skripsiBE.app.views import roles
from skripsiBE.app.views import user_groups
from skripsiBE.app.views import user_logs
from skripsiBE.app.views import users
from skripsiBE.app.views import working_hours

urlpatterns = [
    path('admin/', admin.site.urls),

    path('approval-requests/', approval_requests.ApprovalRequestsList),
    path('approval-requests/<int:id>/', approval_requests.ApprovalRequestDetails),

    path('attendance-types/', attendance_types.AttendanceTypesList),
    path('attendance-types/<int:id>/', attendance_types.AttendanceTypeDetails),

    path('groups/', groups.GroupsList),
    path('groups/<int:id>/', groups.GroupDetails),
    
    path('invitation-requests/', invitation_requests.InvitationRequestsList),
    path('invitation-requests/<int:id>/', invitation_requests.InvitationRequestDetails),

    path('roles/', roles.RolesList),
    path('roles/<int:id>/', roles.RoleDetails),
    
    path('user-groups/', user_groups.UserGroupsList),
    path('user-groups/<int:id>/', user_groups.UserGroupDetails),

    path('user-logs/', user_logs.UserLogsList),
    path('user-logs/<int:id>/', user_logs.UserLogDetails),
    
    path('users/', users.UsersList),
    path('users/<int:id>/', users.UserDetails),

    path('working-hours/', working_hours.WorkingHoursList),
    path('working-hours/<int:id>/', working_hours.WorkingHourDetails),
]
