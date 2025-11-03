"""Report models and PDF generation."""

from django.db import models

from orders.models import Order


class Report(models.Model):
    """Report model for lab reports."""

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="report")
    pdf_file = models.FileField(upload_to="reports/", null=True, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="generated_reports",
    )

    class Meta:
        db_table = "reports"
        ordering = ["-generated_at"]

    def __str__(self):
        return f"Report for {self.order.order_no}"
