"""Patient serializers."""

from datetime import date

from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone
from rest_framework import serializers

from .models import Patient
from .services import allocate_patient_mrn


class PatientSerializer(serializers.ModelSerializer):
    """
    Serializes Patient data for API output and validates incoming data.

    This serializer handles the conversion of Patient model instances to JSON
    and validates data for creating and updating patient records. It also
    supports fields for offline registration, allowing patient data to be
    captured on a terminal and synced later.

    The serializer ensures that either a date of birth or age is provided,
    and it can calculate one from the other. It also normalizes phone numbers
    and validates the format of the National ID (CNIC).
    """

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
            "age_years",
            "age_months",
            "age_days",
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
        """
        Validates that the date of birth is not in the future.

        Args:
            value (date): The date of birth to validate.

        Returns:
            date: The validated date of birth.

        Raises:
            serializers.ValidationError: If the date of birth is in the future.
        """
        if value and value > date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value

    def validate_phone(self, value):
        """
        Normalizes and validates a Pakistani mobile phone number.

        The number is normalized by removing spaces and hyphens. It then
        validates that the number starts with a valid prefix ('+92' or '0').

        Args:
            value (str): The phone number to validate.

        Returns:
            str: The normalized phone number.

        Raises:
            serializers.ValidationError: If the phone number format is invalid.
        """
        # Remove spaces and hyphens
        phone = value.replace(" ", "").replace("-", "")
        # Ensure it starts with +92 or 0
        if not phone.startswith(("+92", "0")):
            raise serializers.ValidationError("Phone must start with +92 or 0.")
        return phone

    def validate_cnic(self, value):
        """
        Validates the format of a Pakistani National ID card (CNIC).

        The expected format is '#####-#######-#'. The field is optional,
        so None or an empty string are considered valid.

        Args:
            value (str): The CNIC number to validate.

        Returns:
            str or None: The validated CNIC number or None if it's empty.

        Raises:
            serializers.ValidationError: If the CNIC format is invalid.
        """
        import re

        # Allow None or empty string (optional field)
        if not value:
            return None

        if not re.match(r"^\d{5}-\d{7}-\d$", value):
            raise serializers.ValidationError("CNIC must be in format #####-#######-#")
        return value

    def validate(self, attrs):
        """
        Validates that either DOB or age is provided and calculates missing values.

        This method ensures that a patient record contains either a date of birth
        or at least one age component (years, months, or days). If one is missing,
        it calculates it from the other.

        - If only age is provided, DOB is calculated from the current date.
        - If only DOB is provided, age components are calculated.

        Args:
            attrs (dict): The dictionary of attributes to validate.

        Returns:
            dict: The validated and updated attributes.

        Raises:
            serializers.ValidationError: If neither DOB nor age is provided, or if
                                     the age values are invalid.
        """
        dob = attrs.get('dob')
        age_years = attrs.get('age_years')
        age_months = attrs.get('age_months')
        age_days = attrs.get('age_days')

        # Check if either DOB or at least one age field is provided
        has_dob = dob is not None
        has_age = any([
            age_years is not None,
            age_months is not None,
            age_days is not None
        ])

        if not has_dob and not has_age:
            raise serializers.ValidationError(
                "Either date of birth or at least one age field "
                "(years, months, days) must be provided."
            )

        # If age fields provided but no DOB, calculate DOB
        if has_age and not has_dob:
            years = age_years or 0
            months = age_months or 0
            days = age_days or 0

            today = date.today()
            try:
                # Calculate DOB from age
                attrs["dob"] = today - relativedelta(
                    years=years, months=months, days=days
                )
            except Exception as e:
                raise serializers.ValidationError(
                    f"Invalid age values: {str(e)}"
                ) from e

        # If DOB provided but no age fields, calculate age
        if has_dob and not has_age:
            dob_date = attrs['dob']
            today = date.today()

            # Calculate age components
            delta = relativedelta(today, dob_date)
            attrs['age_years'] = delta.years
            attrs['age_months'] = delta.months
            attrs['age_days'] = delta.days

        return attrs

    def create(self, validated_data):
        """
        Creates a new patient record with support for offline registration.

        This method handles both online and offline patient creation. For offline
        registrations, it uses the `allocate_patient_mrn` service to generate
        a Medical Record Number (MRN) from a terminal-specific range.

        Args:
            validated_data (dict): The validated data for creating a patient.

        Returns:
            Patient: The newly created patient instance.

        Raises:
            serializers.ValidationError: If there are issues with offline registration,
                                     such as an invalid terminal or exhausted MRN range.
        """
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
            # Use safe, user-facing error messages without exposing system details
            error_messages = e.messages if hasattr(e, "messages") else [str(e)]

            # Provide appropriate user-facing messages based on the error content
            for msg in error_messages:
                msg_lower = msg.lower()
                if "required" in msg_lower and "terminal" in msg_lower:
                    raise serializers.ValidationError(
                        {
                            "detail": (
                                "Terminal code is required for offline registration."
                            )
                        }
                    ) from e
                elif "not found" in msg_lower or "not active" in msg_lower:
                    raise serializers.ValidationError(
                        {
                            "detail": (
                                "Invalid or inactive terminal. "
                                "Please verify the terminal configuration."
                            )
                        }
                    ) from e
                elif "exhausted" in msg_lower:
                    raise serializers.ValidationError(
                        {
                            "detail": (
                                "Terminal has exhausted its offline registration "
                                "range. Please contact administrator."
                            )
                        }
                    ) from e

            # Generic error for any other validation issues
            raise serializers.ValidationError(
                {
                    "detail": (
                        "Invalid registration parameters. "
                        "Please check your input and try again."
                    )
                }
            ) from e

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
                ) from e
            raise

        return patient
