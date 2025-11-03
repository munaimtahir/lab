"""Tests for orders app."""

from datetime import date

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from catalog.models import TestCatalog
from patients.models import Patient

from .models import Order

User = get_user_model()


@pytest.mark.django_db
class TestOrderAPI:
    """Test order API endpoints."""

    def setup_method(self):
        """Set up test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="reception",
            password="testpass123",
            role="RECEPTION",
        )
        self.patient = Patient.objects.create(
            full_name="John Doe",
            father_name="James Doe",
            dob=date(1990, 1, 1),
            sex="M",
            phone="03001234567",
            cnic="12345-1234567-1",
            address="123 Main St",
        )
        self.test1 = TestCatalog.objects.create(
            code="CBC",
            name="Complete Blood Count",
            category="Hematology",
            sample_type="Blood",
            price=500.00,
            turnaround_time_hours=24,
        )
        self.test2 = TestCatalog.objects.create(
            code="LFT",
            name="Liver Function Test",
            category="Biochemistry",
            sample_type="Blood",
            price=800.00,
            turnaround_time_hours=48,
        )

    def test_create_order(self):
        """Test creating an order."""
        self.client.force_authenticate(user=self.user)
        data = {
            "patient": self.patient.id,
            "priority": "ROUTINE",
            "test_ids": [self.test1.id, self.test2.id],
            "notes": "Test order",
        }
        response = self.client.post("/api/orders/", data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert "order_no" in response.data
        assert response.data["order_no"].startswith("ORD-")
        assert len(response.data["items"]) == 2

    def test_get_order_detail(self):
        """Test getting order detail."""
        self.client.force_authenticate(user=self.user)
        # Create order first
        order = Order.objects.create(
            patient=self.patient,
            priority="ROUTINE",
        )

        response = self.client.get(f"/api/orders/{order.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["order_no"] == order.order_no

    def test_list_orders(self):
        """Test listing orders."""
        self.client.force_authenticate(user=self.user)
        Order.objects.create(patient=self.patient, priority="ROUTINE")
        Order.objects.create(patient=self.patient, priority="URGENT")

        response = self.client.get("/api/orders/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2

    def test_filter_orders_by_patient(self):
        """Test filtering orders by patient."""
        self.client.force_authenticate(user=self.user)
        patient2 = Patient.objects.create(
            full_name="Jane Doe",
            father_name="James Doe",
            dob=date(1992, 1, 1),
            sex="F",
            phone="03001234568",
            cnic="12345-1234567-2",
            address="124 Main St",
        )
        Order.objects.create(patient=self.patient, priority="ROUTINE")
        Order.objects.create(patient=patient2, priority="URGENT")

        response = self.client.get(f"/api/orders/?patient={self.patient.id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
