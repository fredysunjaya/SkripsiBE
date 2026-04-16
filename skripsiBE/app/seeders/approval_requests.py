from faker import Faker
from skripsiBE.app.models.leave_requests import LeaveRequest
from skripsiBE.app.models.user_groups import UserGroup
from skripsiBE.app.models.users import User
from datetime import timedelta

def ApprovalRequestSeeder():
    usersCount = User.objects.count()
    
    for i in range(usersCount):
        fake = Faker("id_ID")
        approvalsCount = fake.random_int(min=5, max=20)
        
        for j in range(approvalsCount):
            groupId = fake.random_int(min=1, max=10)
            userGroups = UserGroup.objects.filter(group_id=groupId, role_id=2).values_list('user_id', flat=True)
            startDateTime = fake.unique.date_time_between(start_date='-60d', end_date='now')
            
            LeaveRequest.objects.create(
                user_id = i + 1,
                group_id = groupId,
                attendance_type_id =fake.random_int(min=1, max=5),
                supervisor_id = fake.random_element(elements=userGroups),
                start_date_time = startDateTime,
                end_date_time = startDateTime + timedelta(hours=8),
                status = fake.random_element(elements=("pending", "accepted", "rejected", "cancelled")),
                reason = fake.sentence()
            )