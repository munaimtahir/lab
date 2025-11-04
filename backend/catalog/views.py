"""Catalog views."""

from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated

from .models import TestCatalog
from .serializers import TestCatalogSerializer


class IsAdminUser(permissions.BasePermission):
    """Permission class that only allows admin users."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == "ADMIN"


class IsAdminOrReadOnly(permissions.BasePermission):
    """Allow read access to all authenticated users, write access to admins only."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        return request.user.role == "ADMIN"


class TestCatalogListCreateView(generics.ListCreateAPIView):
    """List all tests or create a new test (Admin only for create)."""

    queryset = TestCatalog.objects.all().order_by("code")
    serializer_class = TestCatalogSerializer
    permission_classes = [IsAdminOrReadOnly]

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
    permission_classes = [IsAdminOrReadOnly]
