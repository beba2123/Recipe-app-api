"""
Tests for models
"""
from decimal import Decimal

from core import models
from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch

def create_user(email='user@gmail.com', password='password123'):
    """create and return new user."""
    return get_user_model().objects.create_user(email, password)

class ModelTests(TestCase):
    """Test models."""
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@gmail.com'
        password = 'password1234567890'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email) #checking if the login email and the registered email are the same.
        self.assertTrue(user.check_password(password)) # it going to check the hash password

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_email = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.com', 'test4@example.com'],
        ]
        for email, expected in sample_email:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating user without email raises error."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            'admin@gmail.com',
            'password1234567890',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test create recipe model"""
        user = get_user_model().objects.create_user(
            'test@gmail.com',
            'password1234567890',
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample recipe name',
            time_minutes=5,
            price=Decimal('5'),
            description='Sample recipe description.',
        )
        self.assertEqual(str(recipe), recipe.title)


    def test_create_tag(self):
        """Test tag created correctly"""
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='Tag1')

        self.assertEqual(str(tag), tag.name)

    def test_create_ingredient(self):
        """Test ingredient is created properly"""
        user = create_user()
        ingredient = models.Ingredient.objects.create(user=user, name='sauce')

        self.assertEqual(str(ingredient), ingredient.name)

    @patch('core.models.uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg') #recipe_image_file_path for setting the image path

        self.assertEqual(file_path, f'uploads/recipe/{uuid}.jpg')