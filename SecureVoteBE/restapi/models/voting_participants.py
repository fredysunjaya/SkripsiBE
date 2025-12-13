from django.db import models
from .users import User
from .votings import Voting

# Create your models here.
class VotingParticipant(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    voting = models.ForeignKey(Voting, on_delete=models.RESTRICT)
    
    class Meta:
        db_table = "voting_participants"