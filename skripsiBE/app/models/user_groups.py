from django.db import models
from .users import User
from .roles import Role
from .groups import Group

# Create your models here.
class UserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    group = models.ForeignKey(Group, on_delete=models.RESTRICT)
    role = models.ForeignKey(Group, on_delete=models.RESTRICT)
    
    class Meta:
        db_table = "user_groups"