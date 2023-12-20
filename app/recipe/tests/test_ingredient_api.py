from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import  APIClient
from core.models import Ingredient
from recipe.serializers import IngredientSerializer

Ingredient_URL = reverse('recipe:ingredient-list')

def create_user(email='user@example.com', password='pass123'):
    """create and return a user"""
    return get_user_model().objects.create_user(email=email, password=password)

class PublicIngredientApiTest(TestCase):
    """Test for unauthenticated request."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        '''Test that authentication is required to access the endpoint'''
        res = self.client.get(Ingredient_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateIngredientAPITest(TestCase):
    """Test ingredients can be retrieved by authorized users"""
    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients(self):
        """test retrieving a list of ingredient."""
        Ingredient.objects.create(user=self.user, name='sauce')
        Ingredient.objects.create(user=self.user, name='cheese') #create Two ingredient

        #we have to retrieve the ingredient
        res = self.client.get(Ingredient_URL)
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_user(self):
        """Test that only authenticated user's ingredients are returned."""
        user2 = create_user(email="user2@example.com") #we create unauthenticated user
        Ingredient.objects.create(user=user2, name='Vinegar') #create ingredient for it.
        ingredient = Ingredient.objects.create(user=self.user, name='pepper')#create ingredient for authenticated user.
        res = self.client.get(Ingredient_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(len(res.data[0]['name']), ingredient.name)
        self.assertEqual(len(res.data[0]['id']), ingredient.id)