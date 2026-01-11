from faker import Faker
from skripsiBE.app.models.groups import Group
from skripsiBE.app.models.working_hours import WorkingHours
from skripsiBE.app.models.user_groups import UserGroup
from skripsiBE.app.models.attendance_types import AttendanceType

def GroupSeeder():
    fake = Faker("id_ID")
    groupCount = 10
    
    for i in range(groupCount):
        Group.objects.create(
            name = fake.company(),
            description = fake.text(), 
        )
    
    # WorkingHours Seeder
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for day in days:
        for i in range(groupCount):
            WorkingHours.objects.create(
                group_id = i + 1,
                day = day,
                start_time = fake.time_object(),
                end_time = fake.time_object(),
                is_all_day = fake.boolean(),
            )
    
    # UserGroup Seeder
    for i in range(groupCount):
        # Admin
        UserGroup.objects.create(
            user_id = fake.unique.random_int(min=1, max=300),
            group_id = i + 1,
            role_id = 1,
        )
        
        # Supervisor
        spvCount = fake.random_int(min=1, max=5)
        for j in range(spvCount):
            UserGroup.objects.create(
                user_id = fake.unique.random_int(min=1, max=300),
                group_id = i + 1,
                role_id = 2,
            )
        
        # User
        userCount = fake.random_int(min=10, max=20)
        for j in range(userCount):
            UserGroup.objects.create(
                user_id = fake.unique.random_int(min=1, max=300),
                group_id = i + 1,
                role_id = 3,
            )
    
    # AttendanceType Seeder
    for i in range(groupCount):
        for j in range(5):
            AttendanceType.objects.create(
                name = fake.name(),
                group_id = i + 1,
                remaining_amount = fake.random_int(min=1, max=999),
            )