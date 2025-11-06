"""Sample views."""

from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import UserRole

from .models import Sample, SampleStatus
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
        return Response({"error": "Sample not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.user.role not in [UserRole.PHLEBOTOMY, UserRole.ADMIN]:
        return Response(
            {"error": "Only phlebotomy or admin can collect samples"},
            status=status.HTTP_403_FORBIDDEN,
        )

    sample.status = SampleStatus.COLLECTED
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
        return Response({"error": "Sample not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.user.role not in [
        UserRole.PHLEBOTOMY,
        UserRole.TECHNOLOGIST,
        UserRole.PATHOLOGIST,
        UserRole.ADMIN,
    ]:
        return Response(
            {"error": "Only lab staff can receive samples"},
            status=status.HTTP_403_FORBIDDEN,
        )

    sample.status = SampleStatus.RECEIVED
    sample.received_at = timezone.now()
    sample.received_by = request.user
    sample.save()

    serializer = SampleSerializer(sample)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def reject_sample(request, pk):
    """Reject a sample with a reason."""
    try:
        sample = Sample.objects.get(pk=pk)
    except Sample.DoesNotExist:
        return Response({"error": "Sample not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.user.role not in [
        UserRole.PHLEBOTOMY,
        UserRole.TECHNOLOGIST,
        UserRole.PATHOLOGIST,
        UserRole.ADMIN,
    ]:
        return Response(
            {"error": "Only lab staff can reject samples"},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Can only reject samples that are not already processed
    if sample.status not in [
        SampleStatus.PENDING,
        SampleStatus.COLLECTED,
        SampleStatus.RECEIVED,
    ]:
        return Response(
            {"error": f"Cannot reject sample with status {sample.status}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Rejection reason is required
    rejection_reason = request.data.get("rejection_reason", "").strip()
    if not rejection_reason:
        return Response(
            {"error": "Rejection reason is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    sample.status = SampleStatus.REJECTED
    sample.rejection_reason = rejection_reason
    sample.save()

    serializer = SampleSerializer(sample)
    return Response(serializer.data)
