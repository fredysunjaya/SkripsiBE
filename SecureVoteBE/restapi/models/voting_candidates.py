from django.db import models
from .users import User
from .votings import Voting

class VotingCandidate(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    voting = models.ForeignKey(Voting, on_delete=models.RESTRICT)
    description = models.TextField()
    
    class Meta:
        db_table = "voting_candidates"