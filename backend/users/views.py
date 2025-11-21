"""Views for user authentication and management."""

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
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
    """
    Custom token-based login view that includes user role information.

    This view extends the default `TokenObtainPairView` to use a custom
    serializer (`CustomTokenObtainPairSerializer`), which embeds the user's
    role and other details into the JWT response.
    """

    serializer_class = CustomTokenObtainPairSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    API view to handle user logout by blacklisting the refresh token.

    When a user logs out, their refresh token is added to a blacklist,
    preventing it from being used to generate new access tokens. This
    effectively invalidates the user's session.

    Args:
        request (Request): The request object, containing the refresh token.

    Returns:
        Response: A success message if logout is successful, or an error
                  message if the token is invalid.
    """
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
    """
    API view for listing and creating users.

    This view provides a `GET` method to list all users and a `POST` method
    to create a new user. Access is restricted to admin users. It uses
    different serializers for listing and creation to handle password
    hashing correctly.
    """

    queryset = User.objects.all().order_by("id")
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the request method.

        For `POST` requests (creation), it uses the `UserCreateUpdateSerializer`
        to handle password input. For `GET` requests (listing), it uses the
        standard `UserSerializer`.

        Returns:
            Serializer: The serializer class for the current request.
        """
        if self.request.method == "POST":
            return UserCreateUpdateSerializer
        return UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deactivating a user.

    This view allows admin users to perform `GET`, `PUT`, `PATCH`, and
    `DELETE` operations on a specific user instance. The `DELETE` operation
    is a soft delete, meaning it deactivates the user instead of removing
    them from the database.
    """

    queryset = User.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the request method.

        For `PUT` and `PATCH` requests (updates), it uses the
        `UserCreateUpdateSerializer` to handle potential password changes.
        For `GET` requests, it uses the standard `UserSerializer`.

        Returns:
            Serializer: The serializer class for the current request.
        """
        if self.request.method in ["PUT", "PATCH"]:
            return UserCreateUpdateSerializer
        return UserSerializer

    def perform_destroy(self, instance):
        """
        Performs a soft delete by deactivating the user.

        Instead of permanently deleting the user from the database, this method
        sets the `is_active` flag to `False`. This preserves the user's data
        while preventing them from logging in.

        Args:
            instance (User): The user instance to be deactivated.
        """
        instance.is_active = False
        instance.save()
