"""Result views."""

from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from settings.permissions import (
    user_can_enter_result,
    user_can_publish,
    user_can_verify,
)
from settings.utils import should_skip_verification

from .models import Result
from .serializers import ResultSerializer


class ResultListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating results.

    This view provides `GET` and `POST` methods for listing all results and
    creating new ones. Access is restricted to authenticated users.
    """

    queryset = Result.objects.all().select_related(
        "order_item", "entered_by", "verified_by"
    )
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated]


class ResultDetailView(generics.RetrieveUpdateAPIView):
    """
    API view for retrieving and updating a single result.

    This view allows authenticated users to retrieve the details of a specific
    result or update its information.
    """

    queryset = Result.objects.all().select_related(
        "order_item", "entered_by", "verified_by"
    )
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated]


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def enter_result(request, pk):
    """
    Marks a result as 'ENTERED'.

    This action is typically performed by a technologist. It updates the
    result's status and records the user and time of entry.

    Args:
        request (Request): The request object.
        pk (int): The primary key of the result to be entered.

    Returns:
        Response: The serialized result data if successful, or an error
                  response if the user lacks permission.
    """
    try:
        result = Result.objects.get(pk=pk)
    except Result.DoesNotExist:
        return Response({"error": "Result not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check permission using role-based permission system
    if not user_can_enter_result(request.user):
        return Response(
            {"error": "You do not have permission to enter results"},
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
    """
    Marks a result as 'VERIFIED'.

    This action is typically performed by a pathologist. It serves as a
    check on the entered result before it can be published.

    Args:
        request (Request): The request object.
        pk (int): The primary key of the result to be verified.

    Returns:
        Response: The serialized result data if successful, or an error
                  response if the result is not in the correct state or
                  the user lacks permission.
    """
    try:
        result = Result.objects.get(pk=pk)
    except Result.DoesNotExist:
        return Response({"error": "Result not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check permission using role-based permission system
    if not user_can_verify(request.user):
        return Response(
            {"error": "You do not have permission to verify results"},
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
    """
    Marks a result as 'PUBLISHED'.

    This is the final step in the result workflow, making the result
    officially available. Depending on system settings, this may require
    the result to be 'VERIFIED' first.

    Args:
        request (Request): The request object.
        pk (int): The primary key of the result to be published.

    Returns:
        Response: The serialized result data if successful, or an error
                  response if the result is not in the correct state or
                  the user lacks permission.
    """
    try:
        result = Result.objects.get(pk=pk)
    except Result.DoesNotExist:
        return Response({"error": "Result not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check permission using role-based permission system
    if not user_can_publish(request.user):
        return Response(
            {"error": "You do not have permission to publish results"},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Check workflow settings - if verification is disabled, allow publishing from ENTERED status
    skip_verification = should_skip_verification()
    required_status = "ENTERED" if skip_verification else "VERIFIED"

    if result.status != required_status:
        if skip_verification:
            return Response(
                {"error": "Result must be entered before publishing"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            return Response(
                {"error": "Result must be verified before publishing"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    result.status = "PUBLISHED"
    result.published_at = timezone.now()
    result.save()

    serializer = ResultSerializer(result)
    return Response(serializer.data)
