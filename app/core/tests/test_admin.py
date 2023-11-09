"""
Test for the Django admin modefications.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

class AdminSiteTests(TestCase):
    "Tests for Django Admin."

    def setUp(self):
        """Create User and client."""
        self.client = Client() #allows as http request(put, get..)
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@gmail.com',
            password='password123',
        )
        self.client.force_login(self.admin_user) #for authentice each request made by client with the admin user
        self.user = get_user_model().objects.create_user(
            email='user@gmail.com',
            password='password123',
            name='Test User'
        )

    def test_users_list(self):
        """Test that users are listed on user page."""

        url = reverse('admin:core_user_changelist')  #get the list of all users in core app
        res=self.client.get(url) #get the url from the request as a responce

        self.assertContains(res, self.user.name)   #check if our created user is present in the list
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test that edit user page works correctly."""

        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)