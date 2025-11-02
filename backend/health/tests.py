from django.test import Client, TestCase


class HealthCheckTestCase(TestCase):
    """Test cases for health check endpoint."""

    def setUp(self):
        """Set up test client."""
        self.client = Client()

    def test_health_check(self):
        """Test health check endpoint returns healthy status."""
        response = self.client.get("/api/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "healthy"})
