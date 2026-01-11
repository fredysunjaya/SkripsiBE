from skripsiBE.app.models.roles import Role

def RoleSeeder():
    Role.objects.bulk_create(
        [
            Role(name="admin"),
            Role(name="supervisor"),
            Role(name="user"),
        ]
    )