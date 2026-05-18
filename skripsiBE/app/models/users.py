from django.db import models
from pgvector.django import VectorField


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    face_vector = VectorField(dimensions=512, null=True)

    class Meta:
        db_table = "users"
