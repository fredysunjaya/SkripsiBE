from django.db import models
from .users import User
from .votings import Voting

class VotingChoice(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="user_set")
    voting_id = models.ForeignKey(Voting, on_delete=models.RESTRICT)
    candidate_id = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="candidate_set")
    
    class Meta:
        db_table = "voting_choices"