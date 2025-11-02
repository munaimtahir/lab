"""Patient models."""

from django.core.validators import RegexValidator
from django.db import models


class Patient(models.Model):
    """Patient model with demographics."""

    SEX_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]

    # Validators
    cnic_validator = RegexValidator(
        regex=r"^\d{5}-\d{7}-\d$",
        message="CNIC must be in format #####-#######-#",
    )
    phone_validator = RegexValidator(
        regex=r"^(\+92|0)?3\d{9}$",
        message="Phone must be a valid Pakistani mobile number",
    )

    mrn = models.CharField(
        max_length=20,
        unique=True,
        help_text="Medical Record Number (auto-generated)",
    )
    full_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    dob = models.DateField(help_text="Date of birth")
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    phone = models.CharField(max_length=20, validators=[phone_validator])
    cnic = models.CharField(
        max_length=15,
        validators=[cnic_validator],
        unique=True,
        help_text="National ID in format #####-#######-#",
    )
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "patients"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["mrn"]),
            models.Index(fields=["cnic"]),
            models.Index(fields=["phone"]),
        ]

    def __str__(self):
        return f"{self.mrn} - {self.full_name}"

    def save(self, *args, **kwargs):
        """Generate MRN on first save."""
        if not self.mrn:
            # Generate MRN: PAT-YYYYMMDD-NNNN
            from django.utils import timezone

            today = timezone.now().strftime("%Y%m%d")
            # Get the last patient created today
            last_patient = (
                Patient.objects.filter(mrn__startswith=f"PAT-{today}")
                .order_by("mrn")
                .last()
            )
            if last_patient:
                last_num = int(last_patient.mrn.split("-")[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            self.mrn = f"PAT-{today}-{new_num:04d}"
        super().save(*args, **kwargs)
