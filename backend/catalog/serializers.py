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
