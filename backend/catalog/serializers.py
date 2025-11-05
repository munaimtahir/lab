"""Catalog serializers."""

from rest_framework import serializers

from core.validators import validate_alphanumeric_code

from .models import TestCatalog


class TestCatalogSerializer(serializers.ModelSerializer):
    """Test catalog serializer."""

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
        """Validate test code is alphanumeric."""
        return validate_alphanumeric_code(value, "test code")

    def validate_price(self, value):
        """Validate price is positive."""
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value
