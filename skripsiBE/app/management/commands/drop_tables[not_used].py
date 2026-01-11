from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from skripsiBE.app.models.approval_requests import ApprovalRequest 
from skripsiBE.app.models.attendance_types import AttendanceType 
from skripsiBE.app.models.groups import Group
from skripsiBE.app.models.invitation_requests import InvitationRequest
from skripsiBE.app.models.roles import Role
from skripsiBE.app.models.user_groups import UserGroup
from skripsiBE.app.models.user_logs import UserLog
from skripsiBE.app.models.users import User
from skripsiBE.app.models.working_hours import WorkingHours

class Command(BaseCommand):
    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS user_logs CASCADE;")
            cursor.execute("DROP TABLE IF EXISTS approval_requests CASCADE;")
            cursor.execute("DROP TABLE IF EXISTS invitation_requests CASCADE;")
            cursor.execute("DROP TABLE IF EXISTS attendance_types CASCADE;")
            cursor.execute("DROP TABLE IF EXISTS user_groups CASCADE;")
            cursor.execute("DROP TABLE IF EXISTS working_hours CASCADE;")
            cursor.execute("DROP TABLE IF EXISTS roles CASCADE;")
            cursor.execute("DROP TABLE IF EXISTS groups CASCADE;")
            cursor.execute("DROP TABLE IF EXISTS users CASCADE;")
        
        self.stdout.write(self.style.SUCCESS("All tables dropped successfully."))