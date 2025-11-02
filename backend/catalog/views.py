"""Catalog views."""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import TestCatalog
from .serializers import TestCatalogSerializer


class TestCatalogListView(generics.ListAPIView):
    """List all available tests."""

    queryset = TestCatalog.objects.filter(is_active=True)
    serializer_class = TestCatalogSerializer
    permission_classes = [IsAuthenticated]


class TestCatalogDetailView(generics.RetrieveAPIView):
    """Retrieve a specific test by ID."""

    queryset = TestCatalog.objects.all()
    serializer_class = TestCatalogSerializer
    permission_classes = [IsAuthenticated]
