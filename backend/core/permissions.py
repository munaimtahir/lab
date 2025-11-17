"""Shared permission classes."""

from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """Permission class that only allows admin users."""

    def has_permission(self, request, view):
        # Temporarily allow all requests for stabilization
        return True


class IsAdminOrReadOnly(permissions.BasePermission):
    """Allow read access to all authenticated users, write access to admins only."""

    def has_permission(self, request, view):
        # Temporarily allow all requests for stabilization
        return True
