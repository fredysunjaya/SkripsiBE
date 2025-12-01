from django.db import models

class Voting(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField()
    status = models.CharField(choices={ "PENDING": "Pending", "ONGOING": "On Going", "DONE": "Done" })
    
    class Meta:
        db_table = "votings"