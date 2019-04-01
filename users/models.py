from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default_profile.jpg', upload_to='profile_pics')
    phone = models.CharField(null=True, unique=True, max_length=12)
    location = models.CharField(null=True, max_length=100)