"""serializers for recipe APIS"""

from rest_framework import serializers
from core.models import Recipe, Tag, Ingredient



class IngredientSerializer(serializers.ModelSerializer):
    """Serialize a ingredient model"""
    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']

class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']

class RecipeSerializer(serializers.ModelSerializer):
    """serialize a recipe object"""
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags']
        read_only_fields = ['id']

    def _get_or_create_tags(self, tags, recipe):
        """Create or retrieve new tags from the input data and assign them to the recipe"""
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag, #assign the logged in user for diffrent tag & the reason
                    #**tag we use is incase we change name variable in the future.
                 )
            recipe.tags.add(tag_obj)

    def create(self, validated_data):
        """Create and return a new recipe instance, given the validated data."""

        tags = validated_data.pop('tags', []) #delete tag and assign tags variable
        recipe = Recipe.objects.create(**validated_data) #create recipe without a tag.
        self._get_or_create_tags(tags,recipe)#calling our helper function

        return recipe
    def update(self, instance, validated_data):
        """Handle updating an existing recipe"""
        tags = validated_data.pop('tags', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class RecipeDetailSerializer(RecipeSerializer):
    """Serialize a recipe detail"""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description'] #we add description on the recipe part becouse we want each recipe in datail.

# class TagSerializer(serializers.ModelSerializer):
#     """Serializer for tag objects"""

#     class Meta:
#         model = Tag
#         fields = ['id', 'name']
#         read_only_fields = ['id']