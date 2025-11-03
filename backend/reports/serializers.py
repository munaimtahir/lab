"""Report serializers."""

from rest_framework import serializers

from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    """Report serializer."""

    class Meta:
        model = Report
        fields = [
            "id",
            "order",
            "pdf_file",
            "generated_at",
            "generated_by",
        ]
        read_only_fields = ["id", "generated_at", "generated_by"]
