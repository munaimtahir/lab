"""Catalog serializers."""

from rest_framework import serializers

from core.validators import validate_alphanumeric_code

from .models import TestCatalog


class TestCatalogSerializer(serializers.ModelSerializer):
    """
    Serializes `TestCatalog` data for API responses.

    This serializer converts `TestCatalog` model instances into JSON format
    for listing and retrieving test catalog items. It also validates the
    data when creating or updating catalog entries.
    """

    class Meta:
        model = TestCatalog
        fields = [
            "id",
            "code",
            "name",
            "description",
            "category",
            "sample_type",
            "price",
            "turnaround_time_hours",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_code(self, value):
        """
        Validates that the test code is alphanumeric.

        Args:
            value (str): The test code to validate.

        Returns:
            str: The validated test code.
        """
        return validate_alphanumeric_code(value, "test code")

    def validate_price(self, value):
        """
        Validates that the price is a positive number.

        Args:
            value (Decimal): The price to validate.

        Returns:
            Decimal: The validated price.

        Raises:
            serializers.ValidationError: If the price is not greater than 0.
        """
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value
