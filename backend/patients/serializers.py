"""Patient serializers."""

from datetime import date

from rest_framework import serializers
from django.db import IntegrityError
from django.utils import timezone
from django.core.exceptions import ValidationError

from .models import Patient
from .services import allocate_patient_mrn


class PatientSerializer(serializers.ModelSerializer):
    """Patient serializer with validation and offline registration support."""

    # Write-only fields for offline registration
    origin_terminal_code = serializers.CharField(
        write_only=True,
        required=False,
        help_text="Terminal code for offline registration",
    )
    offline = serializers.BooleanField(
        write_only=True,
        default=False,
        help_text="True if this is an offline registration",
    )

    class Meta:
        model = Patient
        fields = [
            "id",
            "mrn",
            "full_name",
            "father_name",
            "dob",
            "sex",
            "phone",
            "cnic",
            "address",
            "origin_terminal",
            "is_offline_entry",
            "synced_at",
            "created_at",
            "updated_at",
            # Write-only fields
            "origin_terminal_code",
            "offline",
        ]
        read_only_fields = [
            "id",
            "mrn",
            "origin_terminal",
            "is_offline_entry",
            "synced_at",
            "created_at",
            "updated_at",
        ]

    def validate_dob(self, value):
        """Validate that date of birth is not in the future."""
        if value > date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value

    def validate_phone(self, value):
        """Normalize phone number."""
        # Remove spaces and hyphens
        phone = value.replace(" ", "").replace("-", "")
        # Ensure it starts with +92 or 0
        if not phone.startswith(("+92", "0")):
            raise serializers.ValidationError("Phone must start with +92 or 0.")
        return phone

    def validate_cnic(self, value):
        """Validate CNIC format."""
        import re

        if not re.match(r"^\d{5}-\d{7}-\d$", value):
            raise serializers.ValidationError("CNIC must be in format #####-#######-#")
        return value

    def create(self, validated_data):
        """Create a patient with offline registration support."""
        # Extract offline-specific fields
        origin_terminal_code = validated_data.pop("origin_terminal_code", None)
        offline = validated_data.pop("offline", False)

        # Allocate MRN using the service
        try:
            mrn, origin_terminal, is_offline_entry = allocate_patient_mrn(
                origin_terminal_code=origin_terminal_code,
                offline=offline,
            )
        except ValidationError as e:
            # Handle expected validation errors from the service
            raise serializers.ValidationError({"detail": str(e)})

        # Set offline-related fields
        if mrn is not None:
            validated_data["mrn"] = mrn
        if origin_terminal is not None:
            validated_data["origin_terminal"] = origin_terminal
        validated_data["is_offline_entry"] = is_offline_entry

        # For offline sync, set synced_at to now
        if offline and is_offline_entry:
            validated_data["synced_at"] = timezone.now()

        # Create the patient
        try:
            patient = Patient.objects.create(**validated_data)
        except IntegrityError as e:
            if "mrn" in str(e).lower() or "unique" in str(e).lower():
                raise serializers.ValidationError(
                    {
                        "detail": "Registration number already exists. "
                        "Please check offline ranges or contact admin."
                    }
                )
            raise

        return patient
