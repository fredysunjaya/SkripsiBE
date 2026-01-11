from faker import Faker 
from skripsiBE.app.models.user_logs import UserLog

def UserLogSeeder():
    fake = Faker("id_ID")
    
    for i in range(500):
        UserLog.objects.create(
            user_id = fake.random_int(min=1, max=300),
            group_id = fake.random_int(min=1, max=10),
            attendance_type_id = fake.random_int(min=1, max=5),
            start_date_time = fake.date_time(),
            end_date_time = fake.date_time(),
        )