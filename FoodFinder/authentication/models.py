from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_cusine = models.TextField(blank=True)


class FavoriteResteraunts(models.Model):
    name = models.TextField()
    name = models.TextField()
    pass
