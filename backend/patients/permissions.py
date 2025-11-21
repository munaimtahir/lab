"""Permission classes for patients app."""

from rest_framework import permissions

from users.models import UserRole


class IsAdminOrReception(permissions.BasePermission):
    """
    Custom permission to only allow access to users with Admin or Reception roles.

    This permission class is used to restrict access to certain API views,
    ensuring that only authorized personnel can perform actions like creating
    or viewing patient records.
    """

    def has_permission(self, request, view):
        """
        Check if the user has permission to access the view.

        Args:
            request (Request): The request object.
            view (APIView): The view being accessed.

        Returns:
            bool: True if the user is authenticated and has the required role,
                  False otherwise.
        """
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in [UserRole.ADMIN, UserRole.RECEPTION]
        )
