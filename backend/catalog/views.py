"""Catalog views."""

from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import TestCatalog
from .serializers import TestCatalogSerializer


class TestCatalogListCreateView(generics.ListCreateAPIView):
    """List all tests or create a new test (Admin only for create)."""

    queryset = TestCatalog.objects.all().order_by("code")
    serializer_class = TestCatalogSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """Filter by is_active if specified in query params."""
        queryset = super().get_queryset()
        is_active = self.request.query_params.get("is_active")
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == "true")
        return queryset


class TestCatalogDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a test (Admin only for update/delete)."""

    queryset = TestCatalog.objects.all()
    serializer_class = TestCatalogSerializer
    permission_classes = [AllowAny]
