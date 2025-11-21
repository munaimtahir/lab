"""Patient views."""

from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Patient
from .permissions import IsAdminOrReception
from .serializers import PatientSerializer


class PatientListCreateView(generics.ListCreateAPIView):
    """
    API view to list patients with search functionality or create a new patient.

    This view supports two main operations:
    - `GET /api/patients/`: Retrieves a list of patients. The list can be
      filtered by a search `query` parameter that matches against the patient's
      full name, phone number, or CNIC.
    - `POST /api/patients/`: Creates a new patient record.

    Access to this view is restricted to users with Admin or Reception roles.
    """

    serializer_class = PatientSerializer
    permission_classes = [IsAdminOrReception]

    def get_queryset(self):
        """
        Returns a queryset of patients, filtered by a search query if provided.

        The `query` parameter in the URL is used to search for patients by
        full name (case-insensitive), phone number (case-insensitive), or
        the beginning of their CNIC.

        Returns:
            QuerySet: A queryset of `Patient` objects.
        """
        queryset = Patient.objects.all()
        query = self.request.query_params.get("query", "").strip()

        if query:
            queryset = queryset.filter(
                Q(full_name__icontains=query)
                | Q(phone__icontains=query)
                | Q(cnic__startswith=query)
            )

        return queryset

    def create(self, request, *args, **kwargs):
        """
        Handles the creation of a new patient.

        This method processes the POST request to create a new patient record.
        It uses the `PatientSerializer` to validate the incoming data and
        create the patient.

        Args:
            request (Request): The request object containing the patient data.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A response with the created patient's data and a 201
                      status code, or an error response if validation fails.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class PatientDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve the details of a specific patient.

    This view supports `GET /api/patients/:id/`, allowing retrieval of a single
    patient record by their unique ID.

    Access to this view is restricted to users with Admin or Reception roles.
    """

    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAdminOrReception]
