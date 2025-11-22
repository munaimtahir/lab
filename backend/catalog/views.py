"""Catalog views."""

from rest_framework import generics

from core.permissions import IsAdminOrReadOnly

from .models import TestCatalog
from .serializers import TestCatalogSerializer


class TestCatalogListCreateView(generics.ListCreateAPIView):
    """
    List all tests or create a new test.

    Allows for the retrieval of a list of all test catalog items and the
    creation of new test catalog items. Creation is restricted to admin users.

    Filtering:
    - `is_active` (boolean): Filters tests based on their active status.
    """

    queryset = TestCatalog.objects.all().order_by("code")
    serializer_class = TestCatalogSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        """
        Optionally filters the queryset by `is_active` status.

        Returns:
            QuerySet: The filtered queryset of `TestCatalog` objects.
        """
        queryset = super().get_queryset()
        is_active = self.request.query_params.get("is_active")
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == "true")
        return queryset


class TestCatalogDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a test.

    Provides endpoints for retrieving the details of a specific test, as well as
    updating or deleting it. Update and delete operations are restricted to admin
    users.
    """

    queryset = TestCatalog.objects.all()
    serializer_class = TestCatalogSerializer
    permission_classes = [IsAdminOrReadOnly]
