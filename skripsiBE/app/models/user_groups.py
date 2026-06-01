from django.db import models
from .users import User
from .roles import Role
from .groups import Group


# Create your models here.
class UserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "user_groups"
        indexes = [
            models.Index(fields=["user", "group", "role"]),
        ]
