"""Result models for test results and verification."""

from django.db import models

from orders.models import OrderItem


class ResultStatus(models.TextChoices):
    """
    Enumeration for the status of a test result.

    This class defines the workflow stages for a result, from its initial
    draft to final publication.
    """

    DRAFT = "DRAFT", "Draft"
    ENTERED = "ENTERED", "Entered"
    VERIFIED = "VERIFIED", "Verified"
    PUBLISHED = "PUBLISHED", "Published"


class Result(models.Model):
    """
    Represents the result of a single test for an order item.

    This model stores the value of a test, its units, and reference range.
    It also tracks the result's progress through the entry, verification,
    and publication workflow, recording which user performed each action and
    when.

    Attributes:
        order_item (OrderItem): The order item this result is for.
        value (str): The value of the test result (e.g., '12.5', 'Positive').
        unit (str): The unit of measurement (e.g., 'g/dL').
        reference_range (str): The normal range for this test.
        flags (str): Flags indicating if the result is high, low, or normal.
        status (str): The current status of the result in the workflow.
        entered_by (User): The user who entered the result.
        verified_by (User): The user who verified the result.
    """

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
