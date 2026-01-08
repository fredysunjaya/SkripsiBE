from django.db import models

class WorkType(models.Model):
    workTypes = {
        "remote": "Remote",
        "on-site": "On-Site"
    }
    
    name = models.CharField(max_length=255, choices=workTypes)
    
    class Meta:
        db_table = "work_types"