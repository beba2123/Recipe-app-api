"""
Test for the Django admin modefications.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

class AdminSiteTests(TestCase):
    "Tests for Django Admin."

    def setup(self):
        """"""