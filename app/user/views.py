"""
Views for the user API.
"""
from rest_framework import generics
# it provides generics class based views that simplify the implementation of common patterns.
from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView): #CreateAPIView that handle the creation of new model instances and it corrspond to the HTTP POST method.
    """Create a new user in the system."""
    serializer_class = UserSerializer

