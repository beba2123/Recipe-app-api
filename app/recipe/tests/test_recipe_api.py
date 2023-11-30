
"""TEST FOR  RECIPE API."""

from  decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Recipe


RECIPES_URL = reverse('recipe:recipe-list')

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

class PublicRecipesApiTests(TestCase):
    """for unauthenticated API tests."""

    def setUp(self):
        self.client = APIClient

    def test_auth_required(self):
        """Test that authentication is required for retrieving tags."""
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)