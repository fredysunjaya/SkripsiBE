from django.contrib import admin
from .models.users import *
from .models.votings import *
from .models.voting_candidates import *
from .models.voting_choices import *
from .models.voting_participants import *

# Register your models here.
admin.site.register(User)
admin.site.register(Voting)
admin.site.register(VotingCandidate)
admin.site.register(VotingChoice)
admin.site.register(VotingParticipant)