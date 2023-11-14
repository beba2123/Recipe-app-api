"""
Test for user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL  = reverse('user:create') #'user -> appname 'create -> url name.''
TOKEN_URL = reverse('user:token')
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

    def test_user_with_email_exists_error(self):
        """Test that email already exists in database error"""
        payload = {'email':'test@gmail.com','password':'testpass','name':'test'}
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST) #FOR TELLING THAT EMAIL IS EXIST.

    def test_password_too_short_error(self):
        """Test that password must be more than 5 characters"""
        payload ={'email':'test@gmail.com','password':'pw', 'name':'test'}
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = get_user_model().objects.filter(
            email=payload['email']
        ).exists() #filter out the the user by using payload email.
        self.assertFalse(user_exist) #checking if the user isnot exist

    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        user_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'test-user-password123',
        }
        create_user(**user_details)

        payload = {
            'email':user_details['email'],
            'password':user_details['password'],
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test that token is not created when invalid credentials are given."""
        create_user(email='test@example',password='password123')
        payload = {'email':'test@example',
                   'password': 'badpass',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # def  test_create_token_blank_password(self):
    #     """Test that token is not created when blank password is provided."""
    #     payload ={'email':'test@example',
    #               'password': '',
    #     }

    #     res = self.client.post(TOKEN_URL, payload)
    #     self.assertIn('token', res.data)
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)