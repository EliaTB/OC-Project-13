from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Deal, DealImages


class DealsViewsTestCase(TestCase):

    def setUp(self):
        Testuser = User.objects.create(username='testuser', password="password")

        Deal.objects.create(
            name='TestDeal',
            category=1,
            short_description='testDescription',
            content='this is my test deal',
            location='testLocation',
            thumbnail='default.jpg',
            author=Testuser
        )


    def test_home(self):
        resp = self.client.get(reverse('deals:home'))
        self.assertEqual(resp.status_code, 200)


    def test_deal_detail(self):
        resp = self.client.get(reverse('deals:deal-detail', kwargs={'deal_id': 1}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['object'].name, 'TestDeal')
        self.assertEqual(resp.context['object'].category, 1)


    def test_DealList(self):
        resp = self.client.get(reverse('deals:deals'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context['deals'])


    def test_DealSearch(self):
        resp = self.client.get(reverse('deals:deals-search'), {'query': 'testLocation'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context['deals'])

        resp = self.client.get(reverse('deals:deals-search'), {'query': 'badLocation'})
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.context['deals'])


    def test_DealCategory(self):
        resp = self.client.get(reverse('deals:deals-category', kwargs={'category': 1}))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context['deals'])

        resp = self.client.get(reverse('deals:deals-category', kwargs={'category': 0}))
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.context['deals'])


    def test_autocomplete(self):
        resp = self.client.get(reverse('deals:autocomplete'),
            {'term': "te"},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(resp.content, b'["testLocation"]')

        resp = self.client.get(reverse('deals:autocomplete'),
            {'term': "ba"},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(resp.content, b'[]')