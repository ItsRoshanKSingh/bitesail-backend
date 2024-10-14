from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from .serializers import UserSerializer, AuthTokenSerializer


# View for handling user registration
class CreateUserView(generics.CreateAPIView):
    """
    API view to handle user registration.

    This view allows users to create new accounts by submitting their name, email, and password.
    It processes the user data using the `UserSerializer`. Once the user is created, the API
    responds with the created user data but does NOT generate or return an authentication token.

    To obtain an authentication token, the user needs to make a separate request to the
    `CreateTokenView` after successful registration.
    """

    # Serializer class for processing user data
    serializer_class = UserSerializer


# View for generating an authentication token
class CreateTokenView(ObtainAuthToken):
    """
    API view to generate a new authentication token for users.

    This view handles user login by taking the user's credentials (email and password), validating them,
    and returning an authentication token if the credentials are valid. The token is then used for
    subsequent authenticated requests.

    After registering via the `CreateUserView`, users need to send their credentials here to receive a
    token that can be used to authenticate further API requests.
    """

    # Use the custom serializer class for validating the user's credentials
    serializer_class = AuthTokenSerializer

    # Set the renderer classes to the default renderer classes (e.g., JSON)
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    View for retrieving details of the authenticated user.

    This view ensures that only authenticated users can access their profile
    information using token-based authentication.
    """

    serializer_class = UserSerializer  # Serializer to handle user data conversion
    authentication_classes = [
        authentication.TokenAuthentication
    ]  # Use token authentication
    permission_classes = [
        permissions.IsAuthenticated
    ]  # Only authenticated users can access this view

    def get_object(self):
        """
        Retrieve and return the authenticated user.
        This method overrides the default behavior to return the current user
        (the user who made the request).
        """
        return self.request.user
