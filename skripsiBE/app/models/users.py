from django.db import models
from pgvector.django import VectorField
class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField()
    face_vector = VectorField(dimensions=512)
    
    class Meta:
        db_table = "users"