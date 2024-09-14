from rest_framework import generics
from apps.user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """
    API view to create a new user.

    This view handles POST requests to create a new user in the system.
    It uses the UserSerializer to validate and serialize the input data.
    """

    serializer_class = UserSerializer
