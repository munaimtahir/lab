"""Views for user authentication and management."""

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from core.permissions import IsAdminUser

from .models import User
from .serializers import (
    CustomTokenObtainPairSerializer,
    UserCreateUpdateSerializer,
    UserSerializer,
)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom login view with role information."""

    serializer_class = CustomTokenObtainPairSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def logout_view(request):
    """Logout view that blacklists the refresh token."""
    try:
        refresh_token = request.data.get("refresh")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response(
            {"detail": "Successfully logged out."}, status=status.HTTP_200_OK
        )
    except Exception:
        return Response(
            {"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST
        )


class UserListCreateView(generics.ListCreateAPIView):
    """List all users or create a new user (Admin only)."""

    queryset = User.objects.all().order_by("id")
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserCreateUpdateSerializer
        return UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or soft-delete a user (Admin only)."""

    queryset = User.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return UserCreateUpdateSerializer
        return UserSerializer

    def perform_destroy(self, instance):
        """Soft delete: deactivate instead of deleting."""
        instance.is_active = False
        instance.save()
