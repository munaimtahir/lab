"""Serializers for user authentication and management."""

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT token serializer that includes the user's role and username.

    This serializer extends the default `TokenObtainPairSerializer` from
    `rest_framework_simplejwt` to add extra user information to the encoded
    token. This allows the frontend to access the user's role and username
    without making an additional API request.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        token["username"] = user.username
        return token

    def validate(self, attrs):
        """
        Validates the token credentials and adds user data to the response.

        In addition to the access and refresh tokens, the response is
        customized to include a serialized representation of the user,
        providing the frontend with all necessary user details upon login.

        Args:
            attrs (dict): The dictionary of attributes to validate.

        Returns:
            dict: The validated data, including tokens and user information.
        """
        data = super().validate(attrs)
        user_serializer = UserSerializer(self.user)
        data["user"] = user_serializer.data
        return data


class UserSerializer(serializers.ModelSerializer):
    """
    Serializes `User` model instances for safe data exposure.

    This serializer is used to convert `User` objects into a format that can
    be easily rendered into JSON for API responses. It includes essential
    user fields but excludes sensitive information like the password.
    """

    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "phone", "first_name", "last_name"]
        read_only_fields = ["id"]


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializes user data for creating and updating user records.

    This serializer is designed for admin-level operations to create new users
    or update existing ones. It includes a write-only `password` field to
    handle password creation and updates securely. It also enforces that
    `email`, `first_name`, and `last_name` are required.
    """

    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "role",
            "phone",
            "first_name",
            "last_name",
            "is_active",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "email": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def create(self, validated_data):
        """
        Creates a new user and hashes the password.

        This method handles the creation of a new user instance from the
        validated data. If a password is provided, it is hashed before saving.
        If no password is provided, a user is created with an unusable password.

        Args:
            validated_data (dict): The validated data for the new user.

        Returns:
            User: The newly created user instance.
        """
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Updates an existing user and optionally updates the password.

        This method updates a user's attributes based on the validated data.
        If a new password is provided in the request, it is hashed and updated.
        Otherwise, the password remains unchanged.

        Args:
            instance (User): The user instance to update.
            validated_data (dict): The validated data for the user.

        Returns:
            User: The updated user instance.
        """
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
