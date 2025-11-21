"""Sample views."""

from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from settings.permissions import user_can_collect

from .models import Sample, SampleStatus
from .serializers import SampleSerializer


class SampleListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating samples.

    This view provides `GET` and `POST` methods for listing all samples and
    creating new ones. Access is restricted to authenticated users.
    """

    queryset = Sample.objects.all().select_related(
        "order_item", "collected_by", "received_by"
    )
    serializer_class = SampleSerializer
    permission_classes = [IsAuthenticated]


class SampleDetailView(generics.RetrieveUpdateAPIView):
    """
    API view for retrieving and updating a single sample.

    This view allows authenticated users to retrieve the details of a specific
    sample or update its information.
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

    This view updates the sample's status to 'COLLECTED' and records the
    user who performed the action and the time of collection. Access is
    controlled by the `user_can_collect` permission.

    Args:
        request (Request): The request object.
        pk (int): The primary key of the sample to be collected.

    Returns:
        Response: The serialized sample data if successful, or an error
                  response if the sample is not found or the user lacks
                  permission.
    """
    try:
        sample = Sample.objects.get(pk=pk)
    except Sample.DoesNotExist:
        return Response({"error": "Sample not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check permission using role-based permission system
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

    This view updates the sample's status to 'RECEIVED' and records the
    user who received it and the time of receipt. Access is restricted
    to lab staff.

    Args:
        request (Request): The request object.
        pk (int): The primary key of the sample to be received.

    Returns:
        Response: The serialized sample data if successful, or an error
                  response if the sample is not found or the user lacks
                  permission.
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
    Rejects a sample and records the reason.

    This view updates the sample's status to 'REJECTED' and saves the
    provided reason. A sample can only be rejected if it has not already
    been processed. Access is restricted to lab staff.

    Args:
        request (Request): The request object, containing the
                           `rejection_reason`.
        pk (int): The primary key of the sample to be rejected.

    Returns:
        Response: The serialized sample data if successful, or an error
                  response if the sample cannot be rejected or the reason
                  is missing.
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
