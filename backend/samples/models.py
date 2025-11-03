"""Sample models for sample collection and tracking."""

from django.db import models

from orders.models import OrderItem


class SampleStatus(models.TextChoices):
    """Sample status choices."""

    PENDING = "PENDING", "Pending Collection"
    COLLECTED = "COLLECTED", "Collected"
    RECEIVED = "RECEIVED", "Received in Lab"
    REJECTED = "REJECTED", "Rejected"


class Sample(models.Model):
    """Sample model for lab specimen tracking."""

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
        """Generate barcode on first save."""
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
