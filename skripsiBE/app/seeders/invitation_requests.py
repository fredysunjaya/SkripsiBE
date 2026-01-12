from faker import Faker
from skripsiBE.app.models.invitation_requests import InvitationRequest
from skripsiBE.app.models.user_groups import UserGroup
from skripsiBE.app.models.users import User

def InvitationRequestSeeder():
    fake = Faker("id_ID")

    usersCount = User.objects.count()
    
    for i in range(usersCount):
        invitationsCount = fake.random_int(min=1, max=10)
        
        for j in range(invitationsCount):
            groupId = fake.random_int(min=1, max=10)
            userGroups = UserGroup.objects.filter(group_id=groupId, role_id=1)
            
            InvitationRequest.objects.create(
                invitee_id = i + 1,
                inviter_id = userGroups[0].user_id,
                group_id = groupId,
                status = fake.random_element(elements=("pending", "accepted", "rejected", "cancelled")),
            )