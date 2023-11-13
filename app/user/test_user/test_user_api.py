"""
Test for user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL  = reverse('user:create')

def create_user(**params):
    """create and return new user."""
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """Test the users api (public). anauthenticated user"""

    def setUp(self):
        self.client=APIClient() #it is for simulate HTTP request(GET, POST, PUT, DELETE, etc)
        #self.client to simulte HTTP requests and interact with your view during the testing process.
        #APIClient() is a part of django rest framework used for providing a set of method to simulate various type of HTTP request for self.client()

    def test_create_user_success(self):
        """Test creating a valid user with payload is successful"""
        payload={'email':'test@gmail.com', 'password': 'testpass', 'name':'test'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data) #to check that the string password is not present in responce data of an HTTP Request.

