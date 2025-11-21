"""Report views."""

from django.core.files.base import ContentFile
from django.http import FileResponse
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from orders.models import Order
from users.models import UserRole

from .models import Report
from .pdf_generator import generate_report_pdf
from .serializers import ReportSerializer


class ReportListView(generics.ListAPIView):
    """
    API view for listing all generated reports.

    This view provides a `GET` method to retrieve a list of all reports that
    have been generated in the system. Access is restricted to authenticated
    users.
    """

    queryset = Report.objects.all().select_related("order", "generated_by")
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]


class ReportDetailView(generics.RetrieveAPIView):
    """
    API view for retrieving a single report.

    This view allows authenticated users to retrieve the details of a specific
    report by its ID.
    """

    queryset = Report.objects.all().select_related("order", "generated_by")
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_report(request, order_id):
    """
    Generates and saves a PDF report for a given order.

    This view triggers the PDF generation process for an order. It checks if
    all results for the order are published and if the user has the correct
    permissions (Pathologist or Admin). The generated PDF is then saved to
    a `Report` model instance.

    Args:
        request (Request): The request object.
        order_id (int): The primary key of the order to generate a report for.

    Returns:
        Response: The serialized report data if successful, or an error
                  response if the report cannot be generated.
    """
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.user.role not in [UserRole.PATHOLOGIST, UserRole.ADMIN]:
        return Response(
            {"error": "Only pathologists can generate reports"},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Check if all results are published
    for item in order.items.all():
        if not item.results.filter(status="PUBLISHED").exists():
            return Response(
                {"error": "All results must be published before report"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    # Generate PDF
    pdf_buffer = generate_report_pdf(order)

    # Create or update report
    report, created = Report.objects.get_or_create(order=order)
    report.generated_by = request.user
    report.pdf_file.save(
        f"report_{order.order_no}.pdf", ContentFile(pdf_buffer.read()), save=True
    )

    serializer = ReportSerializer(report)
    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def download_report(request, pk):
    """
    Allows a user to download a generated report PDF.

    This view serves the PDF file associated with a report, allowing users
    to download it. It returns a `FileResponse` with the appropriate headers
    to trigger a download in the browser.

    Args:
        request (Request): The request object.
        pk (int): The primary key of the report to download.

    Returns:
        FileResponse: The PDF file as a downloadable attachment, or an
                      error response if the report or file is not found.
    """
    try:
        report = Report.objects.get(pk=pk)
    except Report.DoesNotExist:
        return Response({"error": "Report not found"}, status=status.HTTP_404_NOT_FOUND)

    if not report.pdf_file:
        return Response(
            {"error": "PDF file not available"}, status=status.HTTP_404_NOT_FOUND
        )

    return FileResponse(
        report.pdf_file.open("rb"),
        as_attachment=True,
        filename=f"report_{report.order.order_no}.pdf",
    )
