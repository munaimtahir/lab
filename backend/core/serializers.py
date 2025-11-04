"""Serializers for core models."""

from rest_framework import serializers

from .models import LabTerminal


class LabTerminalSerializer(serializers.ModelSerializer):
    """Lab terminal serializer."""

    class Meta:
        model = LabTerminal
        fields = [
            "id",
            "code",
            "name",
            "offline_range_start",
            "offline_range_end",
            "offline_current",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "offline_current", "created_at", "updated_at"]

    def validate_code(self, value):
        """Validate terminal code format."""
        if not value.replace("-", "").replace("_", "").isalnum():
            raise serializers.ValidationError(
                "Terminal code must be alphanumeric (dashes and underscores allowed)."
            )
        return value.upper()

    def validate(self, data):
        """Validate range and check for overlaps."""
        start = data.get("offline_range_start")
        end = data.get("offline_range_end")

        # Get existing values from instance if updating
        if self.instance:
            if start is None:
                start = self.instance.offline_range_start
            if end is None:
                end = self.instance.offline_range_end

        if start is not None and end is not None and start >= end:
            raise serializers.ValidationError(
                {"offline_range_start": "Start must be less than end."}
            )

        # Check for overlapping ranges with other terminals only if we have both values
        if start is not None and end is not None:
            instance = self.instance
            overlapping = LabTerminal.objects.filter(
                offline_range_start__lt=end, offline_range_end__gt=start
            )

            if instance:
                overlapping = overlapping.exclude(pk=instance.pk)

            if overlapping.exists():
                raise serializers.ValidationError(
                    "MRN range overlaps with existing terminal: "
                    f"{overlapping.first().code}"
                )

        return data
