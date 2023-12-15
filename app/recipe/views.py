"""Views for the recipe APIs.
"""
# Create your views here.
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag
from recipe import serializers

class RecipeViewSet(viewsets.ModelViewSet): #the modelViewSet specifically for model
    """Manage recipes in the database."""
    serializer_class =  serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        return self.queryset.filter(user= self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return serialzire class for request."""
        if self.action == 'list': #so the list come from the ModelViewSets
            return serializers.RecipeSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)

class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
     """manage Tags in the database."""
     serializer_class = serializers.TagSerializer
     queryset = Tag.objects.all()
     authentication_classes = [TokenAuthentication]
     permission_classes = [IsAuthenticated]

     def get_queryset(self):
         """return objects for current authenticated user only."""
         return self.queryset.filter(user=self.request.user).order_by('-name')