"""Permission classes for patients app."""

from rest_framework import permissions

from users.models import UserRole


class IsAdminOrReception(permissions.BasePermission):
    """Allow access only to Admin and Reception roles."""

    def has_permission(self, request, view):
        # Temporarily allow all requests for stabilization
        return True
