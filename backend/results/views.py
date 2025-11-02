"""Result views."""

from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import UserRole

from .models import Result
from .serializers import ResultSerializer


class ResultListCreateView(generics.ListCreateAPIView):
    """List or create results."""

    queryset = Result.objects.all().select_related(
        "order_item", "entered_by", "verified_by"
    )
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated]


class ResultDetailView(generics.RetrieveUpdateAPIView):
    """Retrieve or update result."""

    queryset = Result.objects.all().select_related(
        "order_item", "entered_by", "verified_by"
    )
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated]


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def enter_result(request, pk):
    """Enter result (technologist)."""
    try:
        result = Result.objects.get(pk=pk)
    except Result.DoesNotExist:
        return Response(
            {"error": "Result not found"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.user.role not in [UserRole.TECHNOLOGIST, UserRole.ADMIN]:
        return Response(
            {"error": "Only technologists can enter results"},
            status=status.HTTP_403_FORBIDDEN,
        )

    result.status = "ENTERED"
    result.entered_at = timezone.now()
    result.entered_by = request.user
    result.save()

    serializer = ResultSerializer(result)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def verify_result(request, pk):
    """Verify result (pathologist)."""
    try:
        result = Result.objects.get(pk=pk)
    except Result.DoesNotExist:
        return Response(
            {"error": "Result not found"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.user.role not in [UserRole.PATHOLOGIST, UserRole.ADMIN]:
        return Response(
            {"error": "Only pathologists can verify results"},
            status=status.HTTP_403_FORBIDDEN,
        )

    if result.status != "ENTERED":
        return Response(
            {"error": "Result must be entered before verification"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    result.status = "VERIFIED"
    result.verified_at = timezone.now()
    result.verified_by = request.user
    result.save()

    serializer = ResultSerializer(result)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def publish_result(request, pk):
    """Publish result (pathologist)."""
    try:
        result = Result.objects.get(pk=pk)
    except Result.DoesNotExist:
        return Response(
            {"error": "Result not found"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.user.role not in [UserRole.PATHOLOGIST, UserRole.ADMIN]:
        return Response(
            {"error": "Only pathologists can publish results"},
            status=status.HTTP_403_FORBIDDEN,
        )

    if result.status != "VERIFIED":
        return Response(
            {"error": "Result must be verified before publishing"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    result.status = "PUBLISHED"
    result.published_at = timezone.now()
    result.save()

    serializer = ResultSerializer(result)
    return Response(serializer.data)
