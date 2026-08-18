from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class AuthTests(TestCase):
    def test_register_creates_inactive_user(self):
        self.client.post(reverse('register'), {
            'username': 'ahmed', 'email': 'ahmed@test.com',
            'password1': 'StrongPass123!', 'password2': 'StrongPass123!',
        })
        user = User.objects.filter(username='ahmed').first()
        self.assertIsNotNone(user)
        self.assertFalse(user.is_active)   

    def test_login_works_for_active_user(self):
        User.objects.create_user(username='sara', password='StrongPass123!')
        response = self.client.post(reverse('login'), {
            'username': 'sara', 'password': 'StrongPass123!',
        })
        self.assertEqual(response.status_code, 302)   

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertNotEqual(response.status_code, 200)   