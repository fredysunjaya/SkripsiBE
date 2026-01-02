from django.db import models
from .users import User
from .roles import Voting

class Group(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    class Meta:
        db_table = "groups"