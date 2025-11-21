"""Sample serializers."""

from rest_framework import serializers

from .models import Sample


class SampleSerializer(serializers.ModelSerializer):
    """
    Serializes `Sample` data for API responses.

    This serializer converts `Sample` model instances into JSON format,
    making them suitable for use in API views. It exposes all the relevant
    fields for tracking a sample's status and history.
    """

    class Meta:
        model = Sample
        fields = [
            "id",
            "order_item",
            "sample_type",
            "barcode",
            "collected_at",
            "collected_by",
            "received_at",
            "received_by",
            "status",
            "rejection_reason",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "barcode",
            "created_at",
            "updated_at",
        ]
