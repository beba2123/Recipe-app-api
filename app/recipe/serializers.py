"""serializers for recipe APIS"""

from rest_framework import serializers
from core.models import Recipe

class RecipeSerializer(serializers.Serializer):
    """serialize a recipe object"""

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link']
        read_only_fields = ['id']