"""Order views."""

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from patients.permissions import IsAdminOrReception

from .models import Order, OrderStatus
from .serializers import OrderSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    """List orders or create a new order."""

    serializer_class = OrderSerializer
    permission_classes = [IsAdminOrReception]

    def get_queryset(self):
        """Filter orders by patient if provided."""
        queryset = (
            Order.objects.all()
            .select_related("patient")
            .prefetch_related("items__test")
        )
        patient_id = self.request.query_params.get("patient")
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        return queryset

    def create(self, request, *args, **kwargs):
        """Create a new order."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class OrderDetailView(generics.RetrieveAPIView):
    """Retrieve order details."""

    queryset = (
        Order.objects.all().select_related("patient").prefetch_related("items__test")
    )
    serializer_class = OrderSerializer
    permission_classes = [IsAdminOrReception]


@api_view(["POST"])
@permission_classes([IsAdminOrReception])
def cancel_order(request, pk):
    """Cancel an order if no samples have been collected."""
    try:
        order = Order.objects.prefetch_related("items__samples").get(pk=pk)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check if order is already cancelled
    if order.status == OrderStatus.CANCELLED:
        return Response(
            {"error": "Order is already cancelled"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Check if any samples have been collected
    has_collected_samples = False
    for item in order.items.all():
        if item.samples.filter(
            status__in=["COLLECTED", "RECEIVED"]
        ).exists():  # Sample status strings are fine here
            has_collected_samples = True
            break

    if has_collected_samples:
        return Response(
            {"error": "Cannot cancel order after samples have been collected"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Cancel the order
    order.status = OrderStatus.CANCELLED
    order.save()

    # Cancel all order items
    order.items.update(status=OrderStatus.CANCELLED)

    serializer = OrderSerializer(order)
    return Response(serializer.data)
