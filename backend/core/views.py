"""Views for core models."""

from rest_framework import generics, permissions

from .models import LabTerminal
from .serializers import LabTerminalSerializer


class IsAdminUser(permissions.BasePermission):
    """Permission class that only allows admin users."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == "ADMIN"


class LabTerminalListCreateView(generics.ListCreateAPIView):
    """List all terminals or create a new terminal (Admin only)."""

    queryset = LabTerminal.objects.all().order_by("code")
    serializer_class = LabTerminalSerializer
    permission_classes = [IsAdminUser]


class LabTerminalDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a terminal (Admin only)."""

    queryset = LabTerminal.objects.all()
    serializer_class = LabTerminalSerializer
    permission_classes = [IsAdminUser]
