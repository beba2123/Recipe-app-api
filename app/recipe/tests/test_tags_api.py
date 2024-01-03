""" Test for the tags API."""

from decimal import Decimal
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Tag, Recipe
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


def detail_url(tag_id):
    """return Tag detail url"""
    return reverse('recipe:tag-detail', args=[tag_id])


def create_user(email='user@gmail.com', password='password123'):
    """create and return new user."""
    return get_user_model().objects.create_user(email=email, password=password)

class PublicTagsApiTests(TestCase):
    """test for unauthorized API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required to access this API endpoint."""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateTagsApiTests(TestCase):

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving a list of tags."""
        Tag.objects.create(user=self.user, name="Vegan")
        Tag.objects.create(user=self.user, name="Dessert")

        res = self.client.get(TAGS_URL)
        tags = Tag.objects.all().order_by('-name')
        serlizer  = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serlizer.data)

    def test_tags_limited_to_user(self):
        """Test that only returns tags for authenticated user."""
        user2 = create_user(email="user2@gmail.com")
        Tag.objects.create(user=user2, name="Fruity")
        tag = Tag.objects.create(user=self.user, name="Comfort Food")

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code,  status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
        self.assertEqual(res.data[0]['id'], tag.id)

    def test_update_tag(self):
        """for testing the update tag."""
        tag = Tag.objects.create(user= self.user, name='breakfast')

        payload={'name':'coffee'}
        url = detail_url(tag.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, payload['name'])


    def test_delete_tag(self):
        """Test for deleting tag."""
        tag = Tag.objects.create(user=self.user, name='lunch')
        url = detail_url(tag.id)

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        # check if it has been deleted from DB
        tags = Tag.objects.filter(id=tag.id) #first filter out the tag and then
        self.assertFalse(tags.exists()) # then check out if it is exist.

    def test_filter_tags_assigned_to_recipe(self):
        """Test filtering tags by those assigned to recipes."""
        tag1 = Tag.objects.create(user=self.user, name = 'Dessert')
        tag2 =  Tag.objects.create(user=self.user, name='Breakfast')

        recipe1 = Recipe.objects.create(
            title='Dessert Food',
            time_minutes=35,
            price=Decimal('7.00'),
            user=self.user
        )
        recipe1.tags.add(tag1)

        # get all the tags which are associated with any recipe
        res = self.client.get(TAGS_URL, {'assigned_only': 1})
        serializer1 = TagSerializer(tag1)
        serializer2 = TagSerializer(tag2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_filtered_tags_unique(self):
        """Test that returned tags are unique"""
        tag = Tag.objects.create(user=self.user,name='Breakfast')
        Tag.objects.create(user=self.user(),name='Dessert')

        recipe1 = Recipe.objects.create(
            title='Dessert Food',
            time_minutes=35,
            price=Decimal('7.00'),
            user=self.user
        )
        recipe2 = Recipe.objects.create(
            title="BreakFast",
            time_minutes=60,
            price=Decimal("9.00"),
            user=self.user
        )

        recipe1.tags.add(tag)
        recipe2.tags.add(tag)

        res = self.client.get(TAGS_URL, {'assigned_only':1})
        
        self.assertEqual(len(res.data), 1)