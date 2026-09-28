# apps/dashboard/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class DashboardTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='teste', password='SenhaForte_123!'
        )

    def test_dashboard_requer_login(self):
        response = self.client.get(reverse('dashboard:index'))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_logado(self):
        self.client.login(username='teste', password='SenhaForte_123!')
        response = self.client.get(reverse('dashboard:index'))
        self.assertEqual(response.status_code, 200)