"""Views for settings app."""

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import RolePermission, WorkflowSettings
from .serializers import RolePermissionSerializer, WorkflowSettingsSerializer


class WorkflowSettingsView(APIView):
    """
    View for workflow settings (singleton).
    
    GET: Return current workflow settings
    PUT: Update workflow settings
    """

    def get(self, request):
        """Get current workflow settings."""
        settings = WorkflowSettings.load()
        serializer = WorkflowSettingsSerializer(settings)
        return Response(serializer.data)

    def put(self, request):
        """Update workflow settings."""
        settings = WorkflowSettings.load()
        serializer = WorkflowSettingsSerializer(settings, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RolePermissionListView(generics.ListAPIView):
    """List all role permissions."""

    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer


class RolePermissionUpdateView(APIView):
    """
    Bulk update role permissions.
    
    Accepts a list of role permission objects and updates them.
    """

    def put(self, request):
        """Bulk update role permissions."""
        permissions_data = request.data
        if not isinstance(permissions_data, list):
            return Response(
                {"error": "Expected a list of permissions"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        updated_permissions = []
        for perm_data in permissions_data:
            role = perm_data.get("role")
            if not role:
                continue

            permission, created = RolePermission.objects.get_or_create(role=role)
            serializer = RolePermissionSerializer(
                permission, data=perm_data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                updated_permissions.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(updated_permissions)
