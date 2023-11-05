"""
Tests for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test models."""
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@gmail.com'
        password = 'password1234567890'
        user = get_user_model().objects.create(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email) #checking if the login email and the registered email are the same.
        self.assertTrue(user.check_password(password)) # it going to check the hash password