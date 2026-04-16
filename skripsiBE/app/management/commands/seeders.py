from django.core.management.base import BaseCommand, CommandError
from skripsiBE.app.seeders.users import UserSeeder
from skripsiBE.app.seeders.groups import GroupSeeder
from skripsiBE.app.seeders.roles import RoleSeeder
from skripsiBE.app.seeders.user_logs import UserLogSeeder

class Command(BaseCommand):
    def handle(self, *args, **options):
        UserSeeder()
        RoleSeeder()
        GroupSeeder()
        UserLogSeeder()
        
        self.stdout.write(self.style.SUCCESS("Seeding completed successfully."))