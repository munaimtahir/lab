"""Patient serializers."""

from datetime import date

from rest_framework import serializers

from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    """Patient serializer with validation."""

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
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "mrn", "created_at", "updated_at"]

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
