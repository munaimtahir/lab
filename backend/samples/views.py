"""Sample views."""

from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import UserRole

from .models import Sample
from .serializers import SampleSerializer


class SampleListCreateView(generics.ListCreateAPIView):
    """List or create samples."""

    queryset = Sample.objects.all().select_related(
        "order_item", "collected_by", "received_by"
    )
    serializer_class = SampleSerializer
    permission_classes = [IsAuthenticated]


class SampleDetailView(generics.RetrieveUpdateAPIView):
    """Retrieve or update sample."""

    queryset = Sample.objects.all().select_related(
        "order_item", "collected_by", "received_by"
    )
    serializer_class = SampleSerializer
    permission_classes = [IsAuthenticated]


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def collect_sample(request, pk):
    """Mark sample as collected."""
    try:
        sample = Sample.objects.get(pk=pk)
    except Sample.DoesNotExist:
        return Response(
            {"error": "Sample not found"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.user.role not in [UserRole.PHLEBOTOMY, UserRole.ADMIN]:
        return Response(
            {"error": "Only phlebotomy or admin can collect samples"},
            status=status.HTTP_403_FORBIDDEN,
        )

    sample.status = "COLLECTED"
    sample.collected_at = timezone.now()
    sample.collected_by = request.user
    sample.save()

    serializer = SampleSerializer(sample)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def receive_sample(request, pk):
    """Mark sample as received in lab."""
    try:
        sample = Sample.objects.get(pk=pk)
    except Sample.DoesNotExist:
        return Response(
            {"error": "Sample not found"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.user.role not in [
        UserRole.TECHNOLOGIST,
        UserRole.PATHOLOGIST,
        UserRole.ADMIN,
    ]:
        return Response(
            {"error": "Only lab staff can receive samples"},
            status=status.HTTP_403_FORBIDDEN,
        )

    sample.status = "RECEIVED"
    sample.received_at = timezone.now()
    sample.received_by = request.user
    sample.save()

    serializer = SampleSerializer(sample)
    return Response(serializer.data)
