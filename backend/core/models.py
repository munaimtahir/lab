"""Core models for configuration and infrastructure."""

from django.core.exceptions import ValidationError
from django.db import models, transaction


class LabTerminal(models.Model):
    """
    Represents a physical workstation/terminal in the lab.

    Each terminal has a reserved numeric range for offline patient registrations.
    When a terminal is offline, it allocates MRNs from its range without
    needing to contact the central server.
    """

    code = models.CharField(
        max_length=50,
        unique=True,
        help_text="Short unique identifier (e.g., 'LAB1-PC', 'RECEP-1')",
    )
    name = models.CharField(
        max_length=255,
        help_text="Human-readable name for this terminal",
    )
    offline_range_start = models.PositiveIntegerField(
        help_text="Start of the offline MRN range (inclusive)"
    )
    offline_range_end = models.PositiveIntegerField(
        help_text="End of the offline MRN range (inclusive)"
    )
    offline_current = models.PositiveIntegerField(
        default=0,
        help_text="Current position in the offline range (0 = unused)",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this terminal is currently active",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "lab_terminals"
        ordering = ["code"]
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"

    def clean(self):
        """Validate that range_start < range_end."""
        if self.offline_range_start >= self.offline_range_end:
            raise ValidationError(
                "offline_range_start must be less than offline_range_end"
            )

    @transaction.atomic
    def get_next_offline_mrn(self) -> int:
        """
        Atomically allocate the next offline MRN from this terminal's range.

        Returns:
            The next available MRN number.

        Raises:
            ValidationError: If the terminal has exhausted its range.
        """
        # Use select_for_update to prevent race conditions
        terminal = LabTerminal.objects.select_for_update().get(pk=self.pk)

        # Determine next number
        if terminal.offline_current == 0:
            next_mrn = terminal.offline_range_start
        else:
            next_mrn = terminal.offline_current + 1

        # Check if we've exhausted the range
        if next_mrn > terminal.offline_range_end:
            raise ValidationError(
                f"Terminal {terminal.code} has exhausted its offline MRN range "
                f"({terminal.offline_range_start}-{terminal.offline_range_end}). "
                f"Please contact administrator to configure a new range."
            )

        # Update the current position
        terminal.offline_current = next_mrn
        terminal.save(update_fields=["offline_current"])

        return next_mrn
