from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


class Deal(models.Model):
	name = models.CharField(max_length=50)
	short_description = models.CharField(max_length=150)
	content = models.TextField()
	location = models.CharField(max_length=100)
	thumbnail = models.ImageField(default='default.jpg', upload_to='deals_pics')
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deals')


	def get_absolute_url(self):
		return reverse('resv:deal-detail', kwargs={'pk': self.pk})