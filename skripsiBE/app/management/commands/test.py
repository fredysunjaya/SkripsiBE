from faker import Faker 
from skripsiBE.app.models.user_logs import UserLog
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker("id_ID")
        
        UserLog.objects.create(
            user_id = fake.random_int(min=1, max=100),
            group_id = fake.random_int(min=1, max=50),
            attendance_type_id = fake.random_int(min=1, max=5),
            start_time = fake.time(),
            end_time = fake.time(),
        )