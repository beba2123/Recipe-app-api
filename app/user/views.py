"""
Views for the user API.
"""
from rest_framework import generics, authentication , permissions
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

class ManageUserView(generics.RetrieveUpdateAPIView): #to use get, put and patch inside the class.
      """Manage the authenticated user"""
      serializer_class = UserSerializer
      authentication_classes  =  [authentication.TokenAuthentication] #for authenticate the user tring to retrive or update
      permission_classes = [permissions.IsAuthenticated] #permmite  the authenticated user

      def get_object(self):
            """Retrieve and return authenticated user"""
            return self.request.user
