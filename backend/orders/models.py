"""Order models."""

from django.db import models

from catalog.models import TestCatalog
from patients.models import Patient


class OrderStatus(models.TextChoices):
    """Order status choices."""

    NEW = "NEW", "New"
    COLLECTED = "COLLECTED", "Collected"
    IN_PROCESS = "IN_PROCESS", "In Process"
    VERIFIED = "VERIFIED", "Verified"
    PUBLISHED = "PUBLISHED", "Published"


class OrderPriority(models.TextChoices):
    """Order priority choices."""

    ROUTINE = "ROUTINE", "Routine"
    URGENT = "URGENT", "Urgent"
    STAT = "STAT", "STAT"


class Order(models.Model):
    """Order model."""

    order_no = models.CharField(max_length=20, unique=True)
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="orders"
    )
    priority = models.CharField(
        max_length=20,
        choices=OrderPriority.choices,
        default=OrderPriority.ROUTINE,
    )
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.NEW,
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "orders"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["order_no"]),
            models.Index(fields=["patient"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.order_no} - {self.patient.full_name}"

    def save(self, *args, **kwargs):
        """Generate order number on first save."""
        if not self.order_no:
            from django.utils import timezone

            today = timezone.now().strftime("%Y%m%d")
            last_order = (
                Order.objects.filter(order_no__startswith=f"ORD-{today}")
                .order_by("order_no")
                .last()
            )
            if last_order:
                last_num = int(last_order.order_no.split("-")[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            self.order_no = f"ORD-{today}-{new_num:04d}"
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """Order item model representing a test in an order."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    test = models.ForeignKey(TestCatalog, on_delete=models.PROTECT)
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.NEW,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "order_items"
        ordering = ["id"]

    def __str__(self):
        return f"{self.order.order_no} - {self.test.name}"
