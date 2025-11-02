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
    """List all reports."""

    queryset = Report.objects.all().select_related("order", "generated_by")
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]


class ReportDetailView(generics.RetrieveAPIView):
    """Retrieve a specific report."""

    queryset = Report.objects.all().select_related("order", "generated_by")
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_report(request, order_id):
    """Generate PDF report for an order."""
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
                {"error": "All test results must be published before generating report"},
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
    return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def download_report(request, pk):
    """Download report PDF."""
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
