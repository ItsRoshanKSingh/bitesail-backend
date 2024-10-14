"""User API Serializers"""

from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user objects.

    This serializer is responsible for validating and serializing user data.
    It ensures that the password field is handled securely by marking it as
    write-only and enforcing a minimum length. During user creation, the
    password is hashed before being saved to the database.
    """

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "name"]
        extra_kwargs = {
            "password": {
                "write_only": True,  # Password field is input only and excluded from output/response
                "min_length": 5,  # Enforces a minimum length for the password
            }
        }

    def create(self, validated_data):
        """
        Create and return a user with an encrypted password.

        This method overrides the default behavior to ensure that passwords
        are hashed before saving. The `create_user` method is used to create
        the user with a hashed password, ensuring that the password is never
        stored in plain text.
        """
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
        Update the user instance, handling password separately
        to ensure it's hashed before being saved.
        """
        password = validated_data.pop(
            "password", None
        )  # Extract and remove password from validated data if it exists

        user = super().update(
            instance, validated_data
        )  # Update user with the remaining data

        if password:
            user.set_password(password)  # Hash and set the new password
            user.save()  # Save the user instance with the updated password

        return user


class AuthTokenSerializer(serializers.Serializer):
    """
    Serializer for user authentication tokens.

    This serializer handles the validation of user credentials (email and password)
    and returns the authenticated user object if the credentials are valid.
    """

    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """
        Validate and authenticate the user.

        This method takes the email and password from the request, authenticates the user,
        and adds the user object to the validated data if the authentication is successful.
        """

        # Retrieve email and password from the provided attributes
        email = attrs.get("email")
        password = attrs.get("password")

        # Authenticate the user using the provided credentials
        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password,
        )

        # If authentication fails, raise a validation error
        if not user:
            msg = _("Unable to authenticate with provided credentials.")
            raise serializers.ValidationError(msg, code="authorization")

        # Add the user object to the validated attributes and return it
        attrs["user"] = user
        return attrs
