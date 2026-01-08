from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField()
    photo = models.FilePathField(path="skripsiBE/static/")
    
    class Meta:
        db_table = "users"