"""Views for settings app."""

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_permissions(request):
    """
    Get permissions for the current user based on their role.
    
    Returns:
        - role: User's role
        - permissions: Dictionary of all permissions for the role
    """
    user = request.user
    
    # Default permissions (all False except for admin)
    default_perms = {
        "can_register": False,
        "can_collect": False,
        "can_enter_result": False,
        "can_verify": False,
        "can_publish": False,
        "can_edit_catalog": False,
        "can_edit_settings": False,
    }
    
    # Admin has all permissions
    if user.role == "ADMIN":
        default_perms = {k: True for k in default_perms}
    else:
        try:
            role_perm = RolePermission.objects.get(role=user.role)
            default_perms = {
                "can_register": role_perm.can_register,
                "can_collect": role_perm.can_collect,
                "can_enter_result": role_perm.can_enter_result,
                "can_verify": role_perm.can_verify,
                "can_publish": role_perm.can_publish,
                "can_edit_catalog": role_perm.can_edit_catalog,
                "can_edit_settings": role_perm.can_edit_settings,
            }
        except RolePermission.DoesNotExist:
            pass  # Use default_perms (all False)
    
    return Response(
        {
            "role": user.role,
            "permissions": default_perms,
        }
    )
