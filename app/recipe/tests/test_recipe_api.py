
"""TEST FOR  RECIPE API."""

from  decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Recipe
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPES_URL = reverse('recipe:recipe-list')

def detail_url(recipe_id):
    """create and return recipe detail url."""
    return reverse('recipe:recipe-detail', args=[recipe_id])

def create_recipe(user, **params):
    """Create and return a sample recipe."""
    defaults = {
        'title': 'Sample recipe',
        'time_minutes': 10,
        'price': Decimal('5'),
        'description': 'Sample description',
        'link':'https://www.tasteofhome.com/recipes/chicken-parmesan/',
    }
    defaults.update(params)

    recipe = Recipe.objects.create(user=user, **defaults) #create an  Recipe instance
    return recipe

def create_user(**params):
     """Create and return a sample user."""
     return get_user_model().objects.create_user(**params)

class PublicRecipesApiTests(TestCase):
    """for unauthenticated API tests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required for retrieving tags."""
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRecipesApiTests(TestCase):
    """For authenticated user API tests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        # self.user = get_user_model().objects.create_user(
        #     'user@gmail.com',
        #     'password123',
        # )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes."""

        create_recipe(user=self.user)
        create_recipe(user=self.user) # create two recipe from authenticated user.
        res  = self.client.get(RECIPES_URL)

        recipes =  Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)  #for serializing multiple instance but if we serialize single  instance 'many=false'
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_list_limited_to_user(self):
        """Test retrieving recipes for the authenticated user."""
        user2 = create_user(email='user2@gmail.com', password='password123')
        # user2 = get_user_model().objects.create_user(
        #     'user2@gmail.com',
        #     'password123',
        # )
        create_recipe(user=user2) #for not authenticate user
        create_recipe(user=self.user) #for authenticate user

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user) #for filtering out recipe for the authenticated user
        serilizer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serilizer.data)

    def test_get_recipe_detail(self):
        """Test get recipe detail."""
        recipe = create_recipe(user=self.user)
        url = detail_url(recipe.id)

        res = self.client.get(url)
        serializer = RecipeDetailSerializer(recipe) # we don't use many b/c we serialize single instance.
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """Test create recipe."""
        payload = {
            'title':'Sample recipe',
            'time_minutes': 10,
            'price': Decimal('5'),
        }
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)

        self.assertEqual(recipe.user, self.user)

    def test_partial_update(self):
        """Test updating a recipe with patch."""
        original_link = 'https://example.com/recipe.pdf'
        recipe = create_recipe(user=self.user, link=original_link, title='Sample Recipe Title.')
        payload = {'title': 'New recipe title'}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.link, original_link)
        self.assertEqual(recipe.user, self.user)