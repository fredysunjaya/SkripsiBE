from faker import Faker
from skripsiBE.app.models.invitation_requests import InvitationRequest
from skripsiBE.app.models.user_groups import UserGroup

def InvitationRequestSeeder():
    fake = Faker("id_ID")
    
    for i in range(50):
        groupId = fake.random_int(min=1, max=10)
        userGroups = UserGroup.objects.filter(group_id=groupId, role_id=1)
        
        InvitationRequest.objects.create(
            invitee_id = fake.random_int(min=1, max=300),
            inviter_id = userGroups[0].user_id,
            group_id = groupId,
            status = fake.random_element(elements=("pending", "accepted", "rejected", "cancelled")),
        )