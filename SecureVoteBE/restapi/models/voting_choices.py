from django.db import models
from .users import User
from .votings import Voting

class VotingChoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="user_set")
    voting = models.ForeignKey(Voting, on_delete=models.RESTRICT)
    candidate = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="candidate_set")
    
    class Meta:
        db_table = "voting_choices"