"""Order models."""

from django.db import models

from catalog.models import TestCatalog
from patients.models import Patient


class OrderStatus(models.TextChoices):
    """
    Enumeration for the status of an order or order item.

    This class defines the various stages an order can go through in its
    lifecycle, from creation to completion.
    """

    NEW = "NEW", "New"
    COLLECTED = "COLLECTED", "Collected"
    IN_PROCESS = "IN_PROCESS", "In Process"
    VERIFIED = "VERIFIED", "Verified"
    PUBLISHED = "PUBLISHED", "Published"
    CANCELLED = "CANCELLED", "Cancelled"


class OrderPriority(models.TextChoices):
    """
    Enumeration for the priority level of an order.

    This class defines the urgency of an order, which can affect how it is
    processed in the lab.
    """

    ROUTINE = "ROUTINE", "Routine"
    URGENT = "URGENT", "Urgent"
    STAT = "STAT", "STAT"


class Order(models.Model):
    """
    Represents a patient's order for one or more lab tests.

    This model is the central record for a test order, linking a patient to the
    tests they need. It tracks the overall status and priority of the order.

    Attributes:
        order_no (str): A unique, auto-generated number for the order.
        patient (Patient): The patient the order belongs to.
        priority (str): The priority of the order (e.g., 'ROUTINE', 'URGENT').
        status (str): The current status of the order (e.g., 'NEW', 'COLLECTED').
        notes (str): Any additional notes about the order.
    """

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
        """
        Overrides the default save method to generate a unique order number.

        If the order is being created and does not have an `order_no`, this
        method generates one in the format `ORD-YYYYMMDD-NNNN`.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
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
    """
    Represents a single test within an `Order`.

    An order can consist of multiple tests, and each test is represented by an
    `OrderItem`. This allows for individual tracking of the status of each
t   est in an order.

    Attributes:
        order (Order): The order this item belongs to.
        test (TestCatalog): The specific test that was ordered.
        status (str): The status of this individual test.
    """

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
