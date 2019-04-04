from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from deals.models import Deal
from .models import Reservation


class RservationsViewsTest(TestCase):

    def setUp(self):
        self.Testuser = User.objects.create(username='testuser', password="password")
        
        Testdeal = Deal.objects.create(
            name='TestDeal',
            category=1,
            location='testLocation',
            author=self.Testuser
        )

        Reservation.objects.create(
            deal=Testdeal,
            user=self.Testuser,
            status=0,
            checkin="2019-04-04",
            checkout="2019-04-05"
        )


    def test_ReservationList(self):
        resp = self.client.get(reverse('reservations:resv-list'))
        self.assertEqual(resp.status_code, 302)
        
        
        self.client.force_login(user=self.Testuser)
        resp = self.client.get(reverse('reservations:resv-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context['reservations'])


    def test_RequestsList(self):
        resp = self.client.get(reverse('reservations:resvreq-list'))
        self.assertEqual(resp.status_code, 302)
        
        
        self.client.force_login(user=self.Testuser)
        resp = self.client.get(reverse('reservations:resvreq-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context['reservations'])



