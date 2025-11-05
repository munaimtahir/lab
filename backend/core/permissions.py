"""Shared permission classes."""

from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """Permission class that only allows admin users."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == "ADMIN"


class IsAdminOrReadOnly(permissions.BasePermission):
    """Allow read access to all authenticated users, write access to admins only."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        return request.user.role == "ADMIN"
