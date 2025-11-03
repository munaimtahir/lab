"""Test catalog models."""

from django.db import models


class TestCatalog(models.Model):
    """Test catalog model for available lab tests."""

    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100)
    sample_type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    turnaround_time_hours = models.IntegerField(help_text="Expected TAT in hours")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "test_catalog"
        ordering = ["code"]
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["category"]),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"
