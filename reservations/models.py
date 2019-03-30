from django.db import models
from deals.models import Deal
from django.contrib.auth.models import User


class Reservation(models.Model):
    REQUESTED = 0
    ACCEPTED = 1
    DENIED = 2
    STATUS = (
        (REQUESTED, ('Requested')),
        (ACCEPTED, ('Accepted')),
        (DENIED, ('Denied')),
    )
    deal = models.ForeignKey(Deal ,on_delete=models.CASCADE, related_name='reservation')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservation')
    status = models.SmallIntegerField(choices=STATUS, null=True)
    checkin = models.DateTimeField()
    checkout = models.DateTimeField()