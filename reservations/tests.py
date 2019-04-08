from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from deals.models import Deal
from .models import Reservation


class RservationsViewsTest(TestCase):

    def setUp(self):
        self.Testuser = User.objects.create(username='testuser', password="password")
        
        self.Testdeal = Deal.objects.create(
            name='TestDeal',
            category=1,
            location='testLocation',
            author=self.Testuser
        )

        Reservation.objects.create(
            deal=self.Testdeal,
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


    def test_ReservationCreate(self):
        resp = self.client.get(reverse('reservations:resv-create', kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 302)

        self.client.force_login(user=self.Testuser)
        resp = self.client.get(reverse('reservations:resv-create', kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 200)

        url = reverse('reservations:resv-create', kwargs={'pk': 1})
        resp = self.client.post(url, {
            'deal': self.Testdeal,
            'user': self.Testuser,
            'status': 0,
            'adult_nb': 2,
            'children_nb': 1,
            'checkin': "2019-04-05",
            'checkout': "2019-04-10"
            })

        self.assertEqual(resp.status_code, 302)
        deal2 = Reservation.objects.get(id=2)
        self.assertEqual(deal2.deal, self.Testdeal)
        self.assertEqual(deal2.status, 0)
        self.assertEqual(deal2.adult_nb, 2)
        self.assertEqual(deal2.children_nb, 1)
        self.assertEqual(deal2.user, self.Testuser)


    def test_accept_confrim(self):
        resp = self.client.get(reverse('reservations:accept_confirm', 
            kwargs={'reservation_id': 1}))
        self.assertEqual(resp.status_code, 302)

        baduser = User.objects.create(username='baduser', password="password")
        self.client.force_login(user=baduser)
        resp = self.client.get(reverse('reservations:accept_confirm', 
            kwargs={'reservation_id': 1}))
        self.assertEqual(resp.status_code, 403)

        self.client.force_login(user=self.Testuser)
        resp = self.client.get(reverse('reservations:accept_confirm', 
            kwargs={'reservation_id': 1}))
        self.assertEqual(resp.status_code, 200)

    def test_refuse_confrim(self):
        resp = self.client.get(reverse('reservations:refuse_confirm',
            kwargs={'reservation_id': 1}))
        self.assertEqual(resp.status_code, 302)

        baduser = User.objects.create(username='baduser', password="password")
        self.client.force_login(user=baduser)
        resp = self.client.get(reverse('reservations:refuse_confirm', 
            kwargs={'reservation_id': 1}))
        self.assertEqual(resp.status_code, 403)

        self.client.force_login(user=self.Testuser)
        resp = self.client.get(reverse('reservations:refuse_confirm', 
            kwargs={'reservation_id': 1}))
        self.assertEqual(resp.status_code, 200)