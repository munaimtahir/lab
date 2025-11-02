"""Patient views."""

from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Patient
from .permissions import IsAdminOrReception
from .serializers import PatientSerializer


class PatientListCreateView(generics.ListCreateAPIView):
    """
    List patients with search or create a new patient.
    
    GET /api/patients?query= - Search patients by name, phone, or CNIC prefix
    POST /api/patients/ - Create a new patient
    """

    serializer_class = PatientSerializer
    permission_classes = [IsAdminOrReception]

    def get_queryset(self):
        """Filter patients by search query."""
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
        """Create a new patient."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class PatientDetailView(generics.RetrieveAPIView):
    """
    Retrieve a patient by ID.
    
    GET /api/patients/:id/ - Get patient details
    """

    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAdminOrReception]
