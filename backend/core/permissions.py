"""Shared permission classes."""

from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow access to users with the 'ADMIN' role.

    This permission is used to restrict access to sensitive API endpoints
    that should only be accessible by system administrators.
    """

    def has_permission(self, request, view):
        """
        Check if the user is authenticated and has the 'ADMIN' role.

        Args:
            request (Request): The request object.
            view (APIView): The view being accessed.

        Returns:
            bool: True if the user is an admin, False otherwise.
        """
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "ADMIN"
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission for read-only access to all authenticated users.

    This permission allows any authenticated user to perform safe methods like
    GET, HEAD, or OPTIONS. However, write operations such as POST, PUT, PATCH,
    and DELETE are restricted to users with the 'ADMIN' role.
    """

    def has_permission(self, request, view):
        """
        Check permissions based on the request method and user role.

        Args:
            request (Request): The request object.
            view (APIView): The view being accessed.

        Returns:
            bool: True if the user has permission, False otherwise.
        """
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        return request.user.role == "ADMIN"
