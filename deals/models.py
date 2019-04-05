from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


class Deal(models.Model):
    APPARTMENT = 0
    HOLIDAY_HOME = 1
    BED_AND_BREAKFAST = 2
    CATEGORY = (
        (APPARTMENT, ('Appartment')),
        (HOLIDAY_HOME, ('Holiday home')),
        (BED_AND_BREAKFAST, ('Bed and breakfast'))
    )
    name = models.CharField(max_length=50)
    category = models.SmallIntegerField(choices=CATEGORY)
    short_description = models.CharField(max_length=150)
    content = models.TextField()
    location = models.CharField(max_length=100)
    thumbnail = models.ImageField(default='default.jpg', upload_to='deals_pics')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deals')


    def get_absolute_url(self):
        return reverse('deals:deal-detail', kwargs={'pk': self.pk})


class DealImages(models.Model):
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name='dealimages')
    image = models.ImageField(null=True, upload_to='deals_pics')