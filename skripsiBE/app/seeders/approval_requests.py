from faker import Faker
from skripsiBE.app.models.approval_requests import ApprovalRequest
from skripsiBE.app.models.user_groups import UserGroup

def ApprovalRequestSeeder():
    fake = Faker("id_ID")
    
    for i in range(100):
        groupId = fake.random_int(min=1, max=10)
        userGroups = UserGroup.objects.filter(group_id=groupId, role_id=2)
        
        ApprovalRequest.objects.create(
            user_id = fake.random_int(min=1, max=300),
            group_id = groupId,
            attendance_type_id =fake.random_int(min=1, max=5),
            supervisor_id = userGroups[0].user_id,
            start_date_time = fake.date_time(),
            end_date_time = fake.date_time(),
            status = fake.random_element(elements=("pending", "accepted", "rejected", "cancelled")),
            reason = fake.sentence()
        )