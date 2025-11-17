"""Views for core models."""

from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import LabTerminal
from .serializers import LabTerminalSerializer


class LabTerminalListCreateView(generics.ListCreateAPIView):
    """List all terminals or create a new terminal (Admin only)."""

    queryset = LabTerminal.objects.all().order_by("code")
    serializer_class = LabTerminalSerializer
    permission_classes = [AllowAny]


class LabTerminalDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a terminal (Admin only)."""

    queryset = LabTerminal.objects.all()
    serializer_class = LabTerminalSerializer
    permission_classes = [AllowAny]
