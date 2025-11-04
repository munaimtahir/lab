"""Catalog serializers."""

from rest_framework import serializers

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
        if not value.replace("-", "").replace("_", "").isalnum():
            raise serializers.ValidationError(
                "Test code must be alphanumeric (dashes and underscores allowed)."
            )
        return value.upper()

    def validate_price(self, value):
        """Validate price is positive."""
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value
