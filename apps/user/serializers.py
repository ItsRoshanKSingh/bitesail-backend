"""User API Serializers"""

from django.contrib.auth import get_user_model
from rest_framework import serializers


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
