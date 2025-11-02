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
        data = response.json()
        self.assertIn("status", data)
        self.assertIn("database", data)
        self.assertIn("cache", data)
        # Status should be healthy or degraded
        self.assertIn(data["status"], ["healthy", "degraded"])
        
    def test_health_check_database_probe(self):
        """Test database connectivity in health check."""
        response = self.client.get("/api/health/")
        data = response.json()
        # Database should be healthy in tests
        self.assertEqual(data["database"], "healthy")
        
    def test_health_check_cache_probe(self):
        """Test cache connectivity in health check."""
        response = self.client.get("/api/health/")
        data = response.json()
        # Cache status should be present
        self.assertIn("cache", data)

