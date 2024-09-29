from django.db import models
from django.contrib.auth.models import User

class FavoriteRestaurant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to User
    name = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.user.username}"
