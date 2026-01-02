from django.db import models

class Role(models.Model):
    roles = [
        ("admin", "Admin"),
        ("supervisor", "Supervisor"),
        ("user", "user"),
    ]
    
    name = models.CharField(max_length=255, choices=roles)
    
    class Meta:
        db_table = "roles"