"""Order views."""

from rest_framework import generics, status
from rest_framework.response import Response

from patients.permissions import IsAdminOrReception

from .models import Order
from .serializers import OrderSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    """List orders or create a new order."""

    serializer_class = OrderSerializer
    permission_classes = [IsAdminOrReception]

    def get_queryset(self):
        """Filter orders by patient if provided."""
        queryset = Order.objects.all().select_related("patient").prefetch_related("items__test")
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

    queryset = Order.objects.all().select_related("patient").prefetch_related("items__test")
    serializer_class = OrderSerializer
    permission_classes = [IsAdminOrReception]
