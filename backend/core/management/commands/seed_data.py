"""Management command to seed demo data."""

from datetime import date

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from catalog.models import TestCatalog
from patients.models import Patient

User = get_user_model()


class Command(BaseCommand):
    """Seed demo data for LIMS."""

    help = "Seed demo data for LIMS"

    def handle(self, *args, **kwargs):
        """Handle the command."""
        self.stdout.write("Seeding demo data...")

        # Create users
        admin, _ = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@alshifa.com",
                "role": "ADMIN",
                "first_name": "Admin",
                "last_name": "User",
            },
        )
        admin.set_password("admin123")
        admin.save()

        reception, _ = User.objects.get_or_create(
            username="reception",
            defaults={
                "email": "reception@alshifa.com",
                "role": "RECEPTION",
                "first_name": "Reception",
                "last_name": "User",
            },
        )
        reception.set_password("reception123")
        reception.save()

        tech, _ = User.objects.get_or_create(
            username="tech",
            defaults={
                "email": "tech@alshifa.com",
                "role": "TECHNOLOGIST",
                "first_name": "Tech",
                "last_name": "User",
            },
        )
        tech.set_password("tech123")
        tech.save()

        pathologist, _ = User.objects.get_or_create(
            username="pathologist",
            defaults={
                "email": "path@alshifa.com",
                "role": "PATHOLOGIST",
                "first_name": "Dr. Muhammad Munaim",
                "last_name": "Tahir",
            },
        )
        pathologist.set_password("path123")
        pathologist.save()

        self.stdout.write(self.style.SUCCESS("✓ Created users"))

        # Create test catalog
        tests_data = [
            {
                "code": "CBC",
                "name": "Complete Blood Count",
                "category": "Hematology",
                "sample_type": "Blood",
                "price": 500.00,
                "turnaround_time_hours": 24,
                "description": "Complete blood count with differential",
            },
            {
                "code": "LFT",
                "name": "Liver Function Test",
                "category": "Biochemistry",
                "sample_type": "Blood",
                "price": 800.00,
                "turnaround_time_hours": 48,
                "description": "Comprehensive liver panel",
            },
            {
                "code": "RFT",
                "name": "Renal Function Test",
                "category": "Biochemistry",
                "sample_type": "Blood",
                "price": 700.00,
                "turnaround_time_hours": 48,
                "description": "Kidney function markers",
            },
            {
                "code": "LIPID",
                "name": "Lipid Profile",
                "category": "Biochemistry",
                "sample_type": "Blood",
                "price": 600.00,
                "turnaround_time_hours": 24,
                "description": "Cholesterol and triglycerides panel",
            },
            {
                "code": "HBA1C",
                "name": "Glycated Hemoglobin",
                "category": "Biochemistry",
                "sample_type": "Blood",
                "price": 900.00,
                "turnaround_time_hours": 72,
                "description": "Diabetes monitoring test",
            },
        ]

        for test_data in tests_data:
            TestCatalog.objects.get_or_create(
                code=test_data["code"], defaults=test_data
            )

        self.stdout.write(
            self.style.SUCCESS(f"✓ Created {len(tests_data)} test catalog items")
        )

        # Create sample patients
        patients_data = [
            {
                "full_name": "Muhammad Ahmed",
                "father_name": "Abdul Rahman",
                "dob": date(1985, 5, 15),
                "sex": "M",
                "phone": "03001234567",
                "cnic": "12345-1234567-1",
                "address": "House 123, Street 4, Islamabad",
            },
            {
                "full_name": "Fatima Zahra",
                "father_name": "Muhammad Ali",
                "dob": date(1990, 8, 20),
                "sex": "F",
                "phone": "03009876543",
                "cnic": "12345-1234567-2",
                "address": "Flat 45, Block B, Lahore",
            },
        ]

        for patient_data in patients_data:
            Patient.objects.get_or_create(
                cnic=patient_data["cnic"], defaults=patient_data
            )

        self.stdout.write(
            self.style.SUCCESS(f"✓ Created {len(patients_data)} sample patients")
        )
        self.stdout.write(self.style.SUCCESS("\nDemo data seeded successfully! 🎉"))
        self.stdout.write("\nDefault users:")
        self.stdout.write("  admin / admin123 (Admin)")
        self.stdout.write("  reception / reception123 (Reception)")
        self.stdout.write("  tech / tech123 (Technologist)")
        self.stdout.write("  pathologist / path123 (Pathologist)")
