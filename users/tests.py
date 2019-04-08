from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UserViewTests(TestCase):


    def setUp(self):
        self.Testuser = User.objects.create(username='testuser', password="password")


    def test_login(self):
        resp = self.client.post(reverse('login'),
            {'username': 'testuser',
            'password': 'password'}, follow=True)
        self.assertEqual(resp.status_code, 200)


    def test_register(self):
        resp = self.client.post(reverse('register'),
            {'username': 'test',
            'email': 'testuser@email.com',
            'password1': 'password',
            'password2' : 'password' }, follow=True)
        self.assertEqual(resp.status_code, 200)


    def test_logout(self):
        self.client.force_login(user=self.Testuser)
        resp = self.client.get(reverse('logout'))
        self.assertEqual(resp.status_code, 200)


    def test_profile(self):      
        resp = self.client.get(reverse('profile'))
        self.assertEqual(resp.status_code, 302)

        self.client.force_login(user=self.Testuser)
        resp = self.client.get(reverse('profile'))
        self.assertEqual(resp.status_code, 200)


    def test_profile(self):       
        resp = self.client.get(reverse('profile', kwargs={'username': 'testuser'}))
        self.assertEqual(resp.status_code, 302)

        self.client.force_login(user=self.Testuser)
        resp = self.client.get(reverse('profile', kwargs={'username': 'testuser'}))
        self.assertEqual(resp.status_code, 200)