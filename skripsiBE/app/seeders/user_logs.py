from faker import Faker 
from skripsiBE.app.models.user_logs import UserLog
from skripsiBE.app.models.users import User
from datetime import timedelta

def UserLogSeeder():
    usersCount = User.objects.count()
    
    for i in range(usersCount):
        fake = Faker("id_ID")
        
        for j in range(60):
            startDateTime = fake.unique.date_time_between(start_date='-60d', end_date='now')
            
            UserLog.objects.create(
                user_id = i + 1,
                group_id = fake.random_int(min=1, max=10),
                attendance_type_id = fake.random_int(min=1, max=5),
                start_date_time = startDateTime,
                end_date_time = startDateTime + timedelta(hours=8)
            )