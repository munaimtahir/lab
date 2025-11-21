"""Catalog views."""

from rest_framework import generics

from core.permissions import IsAdminOrReadOnly

from .models import TestCatalog
from .serializers import TestCatalogSerializer


class TestCatalogListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating test catalog items.

    This view allows any authenticated user to list the available tests,
    but restricts the creation of new tests to admin users. It supports
    filtering the list by `is_active` status.
    """

    queryset = TestCatalog.objects.all().order_by("code")
    serializer_class = TestCatalogSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        """
        Optionally filters the queryset to show only active or inactive tests.

        This method checks for an `is_active` query parameter in the URL.
        If `is_active=true`, it returns only active tests. If `is_active=false`,
        it returns only inactive tests.

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
    API view for retrieving, updating, and deleting a test catalog item.

    This view allows any authenticated user to retrieve the details of a
    specific test. However, updating or deleting a test is restricted to
    admin users.
    """

    queryset = TestCatalog.objects.all()
    serializer_class = TestCatalogSerializer
    permission_classes = [IsAdminOrReadOnly]
