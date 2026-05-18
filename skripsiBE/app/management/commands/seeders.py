from django.core.management.base import BaseCommand, CommandError
from skripsiBE.app.seeders.users import UserSeeder
from skripsiBE.app.seeders.groups import GroupSeeder
from skripsiBE.app.seeders.roles import RoleSeeder
from skripsiBE.app.seeders.user_logs import UserLogSeeder
from skripsiBE.app.seeders.invitation_requests import InvitationRequestSeeder
from skripsiBE.app.seeders.override_requests import OverrideRequestSeeder
from skripsiBE.app.seeders.leave_requests import LeaveRequestSeeder


class Command(BaseCommand):
    def handle(self, *args, **options):
        # UserSeeder()
        # RoleSeeder()
        # GroupSeeder()
        # UserLogSeeder()
        # InvitationRequestSeeder()
        OverrideRequestSeeder()
        LeaveRequestSeeder()

        self.stdout.write(self.style.SUCCESS("Seeding completed successfully."))
