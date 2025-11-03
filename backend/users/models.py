"""User models for authentication and authorization."""

from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    """User role choices."""

    ADMIN = "ADMIN", "Admin"
    RECEPTION = "RECEPTION", "Reception"
    PHLEBOTOMY = "PHLEBOTOMY", "Phlebotomy"
    TECHNOLOGIST = "TECHNOLOGIST", "Technologist"
    PATHOLOGIST = "PATHOLOGIST", "Pathologist"


class User(AbstractUser):
    """Custom user model with role-based permissions."""

    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.RECEPTION,
    )
    phone = models.CharField(max_length=20, blank=True)

    class Meta:
        db_table = "users"
        ordering = ["id"]

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
