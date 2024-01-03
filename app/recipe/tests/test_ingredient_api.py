from decimal import Decimal
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import  APIClient
from core.models import Ingredient
from recipe.serializers import IngredientSerializer
from core.models import Recipe, Ingredient

INGREDIENTS_URL = reverse('recipe:ingredient-list')

def detail_url(ingredient_id):
    """Return ingredient detail URL for given id"""
    return reverse('recipe:ingredient-detail', args=[ingredient_id])

def create_user(email='user@example.com', password='pass123'):
    """create and return a user"""
    return get_user_model().objects.create_user(email=email, password=password)

class PublicIngredientApiTest(TestCase):
    """Test for unauthenticated request."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        '''Test that authentication is required to access the endpoint'''
        res = self.client.get(INGREDIENTS_URL)

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
        res = self.client.get(INGREDIENTS_URL)
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_user(self):
        """Test that only authenticated user's ingredients are returned."""
        user2 = create_user(email="user2@example.com") #we create unauthenticated user
        Ingredient.objects.create(user=user2, name='Vinegar') #create ingredient for it.
        ingredient = Ingredient.objects.create(user=self.user, name='Pepper')#create ingredient for authenticated user.
        res = self.client.get(INGREDIENTS_URL) #retrieve ingredient from database

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)
        self.assertEqual(res.data[0]['id'], ingredient.id)

    def test_update_ingredient(self):
        """Test updating an existing ingredient"""
        ingredient = Ingredient.objects.create(user=self.user, name='pepper')

        payload = {
            'name': 'Salt'
        }

        url = detail_url(ingredient.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        self.assertEqual(ingredient.name, payload['name'])


    def test_delete_ingredient(self):
        """Test for deleting an exsiting ingredient."""
        ingredient = Ingredient.objects.create(user=self.user, name='vanilla')
        url = detail_url(ingredient.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        ingredients = Ingredient.objects.filter(user=self.user)
        self.assertFalse(ingredients.exists())

    def test_filter_ingredients_assigned_to_recipes(self):
        """Test filtering ingredients by those assigned to recipes."""
        Ingredient1 = Ingredient.objects.create(user=self.user, name='Apples')
        Ingredient2 = Ingredient.objects.create(user=self.user, name='Turkey')

        recipe = Recipe.objects.create(
            title="Apple crumble",
            time_minutes=5,
            price=Decimal('10.0'),
            user = self.user
        )
        recipe.ingredients.add(Ingredient1)

        res = self.client.get(INGREDIENTS_URL, {'assigned_only':1})

        serializer1 = IngredientSerializer(Ingredient1)
        serializer2 = IngredientSerializer(Ingredient2)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

