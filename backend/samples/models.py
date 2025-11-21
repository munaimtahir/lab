"""Sample models for sample collection and tracking."""

from django.db import models

from orders.models import OrderItem


class SampleStatus(models.TextChoices):
    """
    Enumeration for the status of a lab sample.

    This class defines the different stages a sample goes through, from
    pending collection to being received in the lab or rejected.
    """

    PENDING = "PENDING", "Pending Collection"
    COLLECTED = "COLLECTED", "Collected"
    RECEIVED = "RECEIVED", "Received in Lab"
    REJECTED = "REJECTED", "Rejected"


class Sample(models.Model):
    """
    Represents a single lab sample (specimen).

    This model tracks a sample from collection to receipt in the lab. Each
    sample is linked to a specific `OrderItem` and has a unique barcode for
    identification.

    Attributes:
        order_item (OrderItem): The order item this sample is for.
        sample_type (str): The type of sample (e.g., 'Blood', 'Urine').
        barcode (str): A unique, auto-generated barcode for the sample.
        status (str): The current status of the sample (e.g., 'PENDING').
        collected_at (datetime): Timestamp of when the sample was collected.
        collected_by (User): The user who collected the sample.
        received_at (datetime): Timestamp of when the sample was received.
        received_by (User): The user who received the sample.
    """

    order_item = models.ForeignKey(
        OrderItem, on_delete=models.CASCADE, related_name="samples"
    )
    sample_type = models.CharField(max_length=50)
    barcode = models.CharField(max_length=50, unique=True)
    collected_at = models.DateTimeField(null=True, blank=True)
    collected_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="collected_samples",
    )
    received_at = models.DateTimeField(null=True, blank=True)
    received_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="received_samples",
    )
    status = models.CharField(
        max_length=20, choices=SampleStatus.choices, default=SampleStatus.PENDING
    )
    rejection_reason = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "samples"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["barcode"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.barcode} - {self.sample_type}"

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to generate a unique barcode.

        If the sample is being created and does not yet have a barcode, this
        method generates one in the format `SAM-YYYYMMDD-NNNN`.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        if not self.barcode:
            # Generate barcode: SAM-YYYYMMDD-NNNN
            from django.utils import timezone

            today = timezone.now().strftime("%Y%m%d")
            last_sample = (
                Sample.objects.filter(barcode__startswith=f"SAM-{today}")
                .order_by("barcode")
                .last()
            )
            if last_sample:
                last_num = int(last_sample.barcode.split("-")[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            self.barcode = f"SAM-{today}-{new_num:04d}"
        super().save(*args, **kwargs)
