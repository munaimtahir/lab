"""Order serializers."""

from rest_framework import serializers

from catalog.serializers import TestCatalogSerializer
from patients.serializers import PatientSerializer

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    """Order item serializer."""

    test_detail = TestCatalogSerializer(source="test", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "test", "test_detail", "status", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class OrderSerializer(serializers.ModelSerializer):
    """Order serializer."""

    items = OrderItemSerializer(many=True, read_only=True)
    patient_detail = PatientSerializer(source="patient", read_only=True)
    test_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=True,
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "order_no",
            "patient",
            "patient_detail",
            "priority",
            "status",
            "notes",
            "items",
            "test_ids",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "order_no", "status", "created_at", "updated_at"]

    def create(self, validated_data):
        """Create order with order items."""
        test_ids = validated_data.pop("test_ids")
        order = Order.objects.create(**validated_data)

        # Create order items
        for test_id in test_ids:
            OrderItem.objects.create(order=order, test_id=test_id)

        return order
