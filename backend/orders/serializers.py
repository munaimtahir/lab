"""Order serializers."""

from django.utils import timezone
from rest_framework import serializers

from catalog.serializers import TestCatalogSerializer
from patients.serializers import PatientSerializer
from samples.models import Sample, SampleStatus
from settings.utils import should_skip_sample_collection, should_skip_sample_receive

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializes `OrderItem` data for API responses.

    This serializer is used as a nested serializer within `OrderSerializer` to
    display the details of each test included in an order. It includes a
    read-only `test_detail` field to provide the full catalog information for
    the test.
    """

    test_detail = TestCatalogSerializer(source="test", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "test", "test_detail", "status", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializes `Order` data for creating and retrieving orders.

    This serializer handles the main `Order` model, and it includes nested
    serialization for the associated `OrderItem` and `Patient` models to
    provide detailed responses. It also accepts a `test_ids` field for
    creating a new order with multiple tests.
    """

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
        """
        Creates a new order, its associated items, and corresponding samples.

        This method overrides the default `create` to handle the creation of
        `OrderItem` and `Sample` objects based on a list of `test_ids`. It also
        checks the system settings to determine if the sample collection and
        receiving steps should be automatically skipped.

        Args:
            validated_data (dict): The validated data for the new order.

        Returns:
            Order: The newly created order instance.
        """
        test_ids = validated_data.pop("test_ids")
        order = Order.objects.create(**validated_data)

        # Get workflow settings
        skip_collection = should_skip_sample_collection()
        skip_receive = should_skip_sample_receive()

        # Create order items and samples
        for test_id in test_ids:
            order_item = OrderItem.objects.create(order=order, test_id=test_id)

            # Auto-create sample for this order item
            sample_status = SampleStatus.PENDING
            collected_at = None
            received_at = None

            # If collection is disabled, mark as collected automatically
            if skip_collection:
                sample_status = SampleStatus.COLLECTED
                collected_at = timezone.now()

            # If both collection and receive are disabled, mark as received
            if skip_collection and skip_receive:
                sample_status = SampleStatus.RECEIVED
                received_at = timezone.now()

            Sample.objects.create(
                order_item=order_item,
                sample_type=order_item.test.sample_type,
                status=sample_status,
                collected_at=collected_at,
                received_at=received_at,
            )

        return order
