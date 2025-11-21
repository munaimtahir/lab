"""Result serializers."""

from rest_framework import serializers

from .models import Result


class ResultSerializer(serializers.ModelSerializer):
    """
    Serializes `Result` data for API responses.

    This serializer converts `Result` model instances into JSON format,
    which is used for displaying result information in the API. It exposes
    all the fields necessary to track a result's value and its progress
    through the verification and publication workflow.
    """

    class Meta:
        model = Result
        fields = [
            "id",
            "order_item",
            "value",
            "unit",
            "reference_range",
            "flags",
            "status",
            "entered_by",
            "entered_at",
            "verified_by",
            "verified_at",
            "published_at",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "entered_by",
            "entered_at",
            "verified_by",
            "verified_at",
            "published_at",
            "created_at",
            "updated_at",
        ]
