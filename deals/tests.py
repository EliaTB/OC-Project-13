from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Deal, DealImages


class DealsViewsTestCase(TestCase):

    def setUp(self):
        self.Testuser = User.objects.create(username='testuser', password="password")

        Deal.objects.create(
            name='Deal1',
            category=1,
            short_description='testDescription',
            content='this is my test deal',
            location='testLocation',
            thumbnail='default.jpg',
            author=self.Testuser
        )


    def test_home(self):
        resp = self.client.get(reverse('deals:home'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context['deals'])


    def test_deal_detail(self):
        resp = self.client.get(reverse('deals:deal-detail', kwargs={'deal_id': 1}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['object'].name, 'Deal1')
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


    def test_DealCreate(self):
        resp = self.client.get(reverse('deals:deal-create'))
        self.assertEqual(resp.status_code, 302)

        self.client.force_login(user=self.Testuser)
        resp = self.client.get(reverse('deals:deal-create'))
        self.assertEqual(resp.status_code, 200)

        url = reverse('deals:deal-create')
        resp = self.client.post(url, {
            'name': 'Deal2',
            'category': 2,
            'short_description': 'testDescription',
            'content': 'this is my second deal',
            'location': 'testLocation',
            'thumbnail': 'default.jpg',
            'author': self.Testuser
            })

        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/deals/2')
        deal2 = Deal.objects.get(id=2)
        self.assertEqual(deal2.name, 'Deal2')
        self.assertEqual(deal2.category, 2)
        self.assertEqual(deal2.author, self.Testuser)



    def test_DealUpdate(self):
        self.client.force_login(user=self.Testuser)
        resp = self.client.get(reverse('deals:deal-update', kwargs={'pk': 2}))
        self.assertEqual(resp.status_code, 404)

        url = reverse('deals:deal-update', kwargs={'pk': 1})
        resp = self.client.post(url, {
            'name': 'Deal1 updated',
            'category': 1,
            'short_description': 'testDescription',
            'content': 'this is my test deal',
            'location': 'testLocation',
            'thumbnail': 'default.jpg',
            'author': self.Testuser
            })


        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/deals/1')
        deal = Deal.objects.get(id=1)
        self.assertEqual(deal.name, 'Deal1 updated')
        self.assertEqual(deal.category, 1)
        self.assertEqual(deal.author, self.Testuser)


    def test_DealUpdate_forbidden(self):
        baduser = User.objects.create(username='baduser', password="password")
        self.client.force_login(user=baduser)
        resp = self.client.get(reverse('deals:deal-update', kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 403)

    
    def test_DealDelete(self):
        self.client.force_login(user=self.Testuser)
        resp = self.client.post(reverse('deals:deal-delete', kwargs={'pk': 2}))
        self.assertEqual(resp.status_code, 404)

        resp = self.client.post(reverse('deals:deal-delete', kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 302)


    def test_DealDelete_forbidden(self):
        baduser = User.objects.create(username='baduser', password="password")
        self.client.force_login(user=baduser)
        resp = self.client.post(reverse('deals:deal-delete', kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 403)