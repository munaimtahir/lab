"""Settings models for system configuration."""

from django.db import models


class WorkflowSettings(models.Model):
    """
    Workflow configuration settings (singleton pattern).

    Controls which workflow steps are enabled:
    - Sample collection step
    - Sample receive step
    - Result verification step
    """

    enable_sample_collection = models.BooleanField(
        default=True,
        help_text="Enable manual sample collection step",
    )
    enable_sample_receive = models.BooleanField(
        default=True,
        help_text="Enable manual sample receive step in lab",
    )
    enable_verification = models.BooleanField(
        default=True,
        help_text="Require verification before publishing results",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "workflow_settings"
        verbose_name = "Workflow Settings"
        verbose_name_plural = "Workflow Settings"

    def __str__(self):
        return "Workflow Settings"

    def save(self, *args, **kwargs):
        """Ensure only one instance exists (singleton pattern)."""
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        """Load or create the singleton instance."""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class RolePermission(models.Model):
    """
    Role-based permissions matrix.

    Maps each role to specific capabilities in the system.
    """

    ROLE_CHOICES = [
        ("ADMIN", "Admin"),
        ("RECEPTION", "Reception"),
        ("PHLEBOTOMY", "Phlebotomy"),
        ("TECHNOLOGIST", "Technologist"),
        ("PATHOLOGIST", "Pathologist"),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        unique=True,
        help_text="User role",
    )
    can_register = models.BooleanField(
        default=False,
        help_text="Can register new patients",
    )
    can_collect = models.BooleanField(
        default=False,
        help_text="Can collect samples",
    )
    can_enter_result = models.BooleanField(
        default=False,
        help_text="Can enter test results",
    )
    can_verify = models.BooleanField(
        default=False,
        help_text="Can verify test results",
    )
    can_publish = models.BooleanField(
        default=False,
        help_text="Can publish test results",
    )
    can_edit_catalog = models.BooleanField(
        default=False,
        help_text="Can edit test catalog",
    )
    can_edit_settings = models.BooleanField(
        default=False,
        help_text="Can edit system settings",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "role_permissions"
        ordering = ["role"]

    def __str__(self):
        return f"{self.get_role_display()} Permissions"
