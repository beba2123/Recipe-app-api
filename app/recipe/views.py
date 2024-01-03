"""Views for the recipe APIs.
"""
# Create your views here.
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import Recipe, Tag, Ingredient
from recipe import serializers



@extend_schema_view(
    list=extend_schema(  #to extend the schema to the list endpoint
        parameters=[
            OpenApiParameter(
                'tags',
                OpenApiTypes.STR,
                description='Comma separated list of IDs to filter',
            ),
            OpenApiParameter(
                'ingredients',
                OpenApiTypes.STR,
                description='Comma-separated list of IDs of ingredients to filter',
            )
        ]
    )
)

class RecipeViewSet(viewsets.ModelViewSet): #the modelViewSet specifically for model
    """Manage recipes in the database."""
    serializer_class =  serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        #for listing string in tags and in ingredient that is separated by comma
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags) #change it to integer
            queryset = queryset.filter(tags__id__in =tag_ids)
            #tags__id__in is telling to lookup to the 'id' fields of related 'tags' model, and filter the
            # the objects based on whether the 'id' value is present in the list of values specified by 'tag_ids'
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        return queryset.filter(user= self.request.user).order_by('-id').distinct()

    def get_serializer_class(self):
        """Return serialzire class for request."""
        if self.action == 'list': #so the list come from the ModelViewSets
            return serializers.RecipeSerializer
        if self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        recipe = self.get_object()  #we use get_object() to access all attributes and methods of the model
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BaseRecipeAttrViewSet(mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """Base view set for handling recipe attributes."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """return objects for current authenticated user only."""
        return self.queryset.filter(user=self.request.user).order_by('-name')



class TagViewSet(BaseRecipeAttrViewSet):
     """manage Tags in the database."""
     serializer_class = serializers.TagSerializer
     queryset = Tag.objects.all()

class IngredientViewSet(BaseRecipeAttrViewSet):
    """Handles creating and updating ingredients."""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()


