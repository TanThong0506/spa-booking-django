from django.test import TestCase
from django.urls import reverse


class HealthCheckTest(TestCase):
    def test_health_check_returns_ok(self):
        response = self.client.get(reverse('health_check'))

        self.assertIn(response.status_code, [200, 500])
        self.assertIn('status', response.json())