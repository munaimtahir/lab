"""Order views."""

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from patients.permissions import IsAdminOrReception

from .models import Order, OrderStatus
from .serializers import OrderSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating orders.

    This view allows users with Admin or Reception roles to list all orders
    or create a new order. The list of orders can be filtered by patient ID.
    """

    serializer_class = OrderSerializer
    permission_classes = [IsAdminOrReception]

    def get_queryset(self):
        """
        Returns a queryset of orders, optionally filtered by patient.

        If a `patient` query parameter is provided, the queryset will only
        include orders for that patient. It also optimizes the query by
        pre-fetching related patient and test data.

        Returns:
            QuerySet: A queryset of `Order` objects.
        """
        queryset = (
            Order.objects.all()
            .select_related("patient")
            .prefetch_related("items__test")
        )
        patient_id = self.request.query_params.get("patient")
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        return queryset

    def create(self, request, *args, **kwargs):
        """
        Handles the creation of a new order.

        This method validates the incoming data using the `OrderSerializer`
        and creates a new order along with its associated items and samples.

        Args:
            request (Request): The request object containing the order data.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A response with the created order's data and a 201
                      status code, or an error response if validation fails.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class OrderDetailView(generics.RetrieveAPIView):
    """
    API view for retrieving the details of a specific order.

    This view allows users with Admin or Reception roles to get the detailed
    information for a single order, including its items and patient data.
    """

    queryset = (
        Order.objects.all().select_related("patient").prefetch_related("items__test")
    )
    serializer_class = OrderSerializer
    permission_classes = [IsAdminOrReception]


@api_view(["POST"])
@permission_classes([IsAdminOrReception])
def cancel_order(request, pk):
    """
    Cancels an order, if possible.

    An order can only be canceled if none of its associated samples have been
    collected. If the cancellation is successful, the order and all its items
    are marked as 'CANCELLED'.

    Args:
        request (Request): The request object.
        pk (int): The primary key of the order to cancel.

    Returns:
        Response: The serialized order data if successful, or an error
                  response if the order cannot be canceled.
    """
    try:
        order = Order.objects.prefetch_related("items__samples").get(pk=pk)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check if order is already cancelled
    if order.status == OrderStatus.CANCELLED:
        return Response(
            {"error": "Order is already cancelled"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Check if any samples have been collected
    has_collected_samples = False
    for item in order.items.all():
        if item.samples.filter(
            status__in=["COLLECTED", "RECEIVED"]
        ).exists():  # Sample status strings are fine here
            has_collected_samples = True
            break

    if has_collected_samples:
        return Response(
            {"error": "Cannot cancel order after samples have been collected"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Cancel the order
    order.status = OrderStatus.CANCELLED
    order.save()

    # Cancel all order items
    order.items.update(status=OrderStatus.CANCELLED)

    serializer = OrderSerializer(order)
    return Response(serializer.data)


@api_view(["PATCH"])
@permission_classes([IsAdminOrReception])
def edit_order_tests(request, pk):
    """
    Edits the tests in an order by adding or removing items.

    Tests can only be edited if the order has not yet progressed to the
    sample collection or results entry stage. This prevents modifications
    that would invalidate the existing workflow.

    Args:
        request (Request): The request object, containing lists of
                           `tests_to_add` and `tests_to_remove`.
        pk (int): The primary key of the order to edit.

    Returns:
        Response: The updated serialized order data if successful, or an
                  error response if the order cannot be edited.
    """
    try:
        order = Order.objects.prefetch_related("items__samples", "items__results").get(
            pk=pk
        )
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check if order is cancelled
    if order.status == OrderStatus.CANCELLED:
        return Response(
            {"error": "Cannot edit a cancelled order"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Check if any samples exist
    has_samples = False
    for item in order.items.all():
        if item.samples.exists():
            has_samples = True
            break

    if has_samples:
        return Response(
            {"error": "Cannot edit tests after samples have been created"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Check if any results exist
    has_results = False
    for item in order.items.all():
        if item.results.exists():
            has_results = True
            break

    if has_results:
        return Response(
            {"error": "Cannot edit tests after results have been created"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Get test modifications from request
    tests_to_add = request.data.get("tests_to_add", [])
    tests_to_remove = request.data.get("tests_to_remove", [])

    if not tests_to_add and not tests_to_remove:
        return Response(
            {"error": "No tests specified for addition or removal"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Validate that we're not removing all tests
    current_test_ids = set(order.items.values_list("test_id", flat=True))
    remaining_tests = current_test_ids - set(tests_to_remove)
    if not remaining_tests and not tests_to_add:
        return Response(
            {"error": "Cannot remove all tests from order"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Remove tests
    if tests_to_remove:
        from .models import OrderItem

        OrderItem.objects.filter(order=order, test_id__in=tests_to_remove).delete()

    # Add tests
    if tests_to_add:
        from .models import OrderItem

        for test_id in tests_to_add:
            # Check if test already exists in order
            if not OrderItem.objects.filter(order=order, test_id=test_id).exists():
                OrderItem.objects.create(order=order, test_id=test_id)

    # Refresh order and return
    order.refresh_from_db()
    serializer = OrderSerializer(order)
    return Response(serializer.data)
