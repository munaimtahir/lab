"""Result models for test results and verification."""

from django.db import models

from orders.models import OrderItem


class ResultStatus(models.TextChoices):
    """Result status choices."""

    DRAFT = "DRAFT", "Draft"
    ENTERED = "ENTERED", "Entered"
    VERIFIED = "VERIFIED", "Verified"
    PUBLISHED = "PUBLISHED", "Published"


class Result(models.Model):
    """Result model for test results."""

    order_item = models.ForeignKey(
        OrderItem, on_delete=models.CASCADE, related_name="results"
    )
    value = models.CharField(max_length=255)
    unit = models.CharField(max_length=50, blank=True)
    reference_range = models.CharField(max_length=255, blank=True)
    flags = models.CharField(
        max_length=50, blank=True, help_text="H=High, L=Low, N=Normal"
    )
    status = models.CharField(
        max_length=20, choices=ResultStatus.choices, default=ResultStatus.DRAFT
    )
    entered_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="entered_results",
    )
    entered_at = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="verified_results",
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "results"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.order_item} - {self.value} {self.unit}"
