"""
Views for the user API.
"""
from rest_framework import generics
# it provides generics class based views that simplify the implementation of common patterns.
from user.serializers import UserSerializer, AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


class CreateUserView(generics.CreateAPIView): #CreateAPIView that handle the creation of new model instances and it corrspond to the HTTP POST method.
    """Create a new user in the system."""
    serializer_class = UserSerializer #specify the serializers to be used for serializing the user data.

class CreateTokenView(ObtainAuthToken): #it has a defualt username and password
        """Create a new auth token for  users """
        serializer_class =  AuthTokenSerializer #wecustomize the serializer by changing to email and password from usrname and password
        renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES