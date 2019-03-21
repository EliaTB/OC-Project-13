from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Deal(models.Model):
	name = models.CharField(max_length=50)
	short_description = models.CharField(max_length=150)
	content = models.TextField()
	location = models.CharField(max_length=100)
	picture = models.URLField()
	date_posted = models.DateTimeField(default=timezone.now)
	rating = models.IntegerField()
	author = models.ForeignKey(User, on_delete=models.CASCADE)
