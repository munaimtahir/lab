"""Sample views."""

from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from settings.permissions import user_can_collect
from users.models import UserRole

from .models import Sample, SampleStatus
from .serializers import SampleSerializer


class SampleListCreateView(generics.ListCreateAPIView):
    """
    Lists and creates samples.
    """

    queryset = Sample.objects.all().select_related(
        "order_item", "collected_by", "received_by"
    )
    serializer_class = SampleSerializer
    permission_classes = [IsAuthenticated]


class SampleDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieves and updates a specific sample.
    """

    queryset = Sample.objects.all().select_related(
        "order_item", "collected_by", "received_by"
    )
    serializer_class = SampleSerializer
    permission_classes = [IsAuthenticated]


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def collect_sample(request, pk):
    """
    Marks a sample as collected.

    Args:
        request: The request object.
        pk (int): The primary key of the sample to collect.

    Returns:
        Response: A response object with the updated sample data or an error message.
    """
    try:
        sample = Sample.objects.get(pk=pk)
    except Sample.DoesNotExist:
        return Response({"error": "Sample not found"}, status=status.HTTP_404_NOT_FOUND)

    if not user_can_collect(request.user):
        return Response(
            {"error": "You do not have permission to collect samples"},
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
    """
    Marks a sample as received in the lab.

    Args:
        request: The request object.
        pk (int): The primary key of the sample to receive.

    Returns:
        Response: A response object with the updated sample data or an error message.
    """
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
    """
    Rejects a sample with a given reason.

    Args:
        request: The request object, containing the `rejection_reason`.
        pk (int): The primary key of the sample to reject.

    Returns:
        Response: A response object with the updated sample data or an error message.
    """
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

    if sample.status not in [
        SampleStatus.PENDING,
        SampleStatus.COLLECTED,
        SampleStatus.RECEIVED,
    ]:
        return Response(
            {"error": f"Cannot reject sample with status {sample.status}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

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
