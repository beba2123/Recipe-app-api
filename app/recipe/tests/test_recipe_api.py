
"""TEST FOR  RECIPE API."""

from  decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Recipe,  Tag, Ingredient
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer
import tempfile, os
from PIL import Image

RECIPES_URL = reverse('recipe:recipe-list')

def detail_url(recipe_id):
    """create and return recipe detail url."""
    return reverse('recipe:recipe-detail', args=[recipe_id])

def upload_image_url(recipe_id):
    """Create a sample image file name for testing."""
    return reverse('recipe:recipe-upload-image', args=[recipe_id])

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

def create_user(**params):
     """Create and return a sample user."""
     return get_user_model().objects.create_user(**params)

class PublicRecipesApiTests(TestCase):
    """for unauthenticated API tests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required for retrieving tags."""
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRecipesApiTests(TestCase):
    """For authenticated user API tests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        # self.user = get_user_model().objects.create_user(
        #     'user@gmail.com',
        #     'password123',
        # )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes."""

        create_recipe(user=self.user)
        create_recipe(user=self.user) # create two recipe from authenticated user.
        res  = self.client.get(RECIPES_URL)

        recipes =  Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)  #for serializing multiple instance but if we serialize single  instance 'many=false'
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_list_limited_to_user(self):
        """Test retrieving recipes for the authenticated user."""
        user2 = create_user(email='user2@gmail.com', password='password123')
        # user2 = get_user_model().objects.create_user(
        #     'user2@gmail.com',
        #     'password123',
        # )
        create_recipe(user=user2) #for not authenticate user
        create_recipe(user=self.user) #for authenticate user

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user) #for filtering out recipe for the authenticated user
        serilizer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serilizer.data)

    def test_get_recipe_detail(self):
        """Test get recipe detail."""
        recipe = create_recipe(user=self.user)
        url = detail_url(recipe.id)

        res = self.client.get(url)
        serializer = RecipeDetailSerializer(recipe) # we don't use many b/c we serialize single instance.
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """Test create recipe."""
        payload = {
            'title':'Sample recipe',
            'time_minutes': 10,
            'price': Decimal('5'),
        }
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)

        self.assertEqual(recipe.user, self.user)

    def test_partial_update(self):
        """Test updating a recipe with patch."""
        original_link = 'https://example.com/recipe.pdf'
        recipe = create_recipe(user=self.user, link=original_link, title='Sample Recipe Title.')
        payload = {'title': 'New recipe title'}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.link, original_link)
        self.assertEqual(recipe.user, self.user)

    def test_full_update(self):
        """Test for fully updating a recipe with put."""
        recipe = create_recipe(user=self.user,
                               title='Sample recipe title',
                               link='https://example.com/recipe.pdf',
                               description='Sample recipe description.')
        payload = {
            'title': 'New recipe title',
            'link': 'https://example.com/new-recipe.pdf',
            'description': 'New recipe description',
            'time_minutes': 25,
            'price': Decimal('5.00'),
        }
        url = detail_url(recipe.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)

    def test_update_user_returns_error(self):
        """Test that updating a recipe with put is not allowed."""
        new_user = create_user(email='user@gmail.com', password='test123')
        recipe = create_recipe(user=self.user)

        payload= {'user':   new_user.id}
        url = detail_url(recipe.id)
        self.client.patch(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.user, self.user)

    def test_delete_recipe(self):
        """Test deleting a recipe."""
        recipe = create_recipe(user=self.user)
        url = detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())

    def test_delete_other_users_recipe_error(self):
        """Test deleting a recipe of other user."""
        other_user = create_user(email='other@gmail.com', password='password123')
        recipe = create_recipe(user=other_user)
        url = detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Recipe.objects.filter(id=recipe.id).exists())

    def test_create_recipe_with_new_tags(self):
        """Test creating a recipe with tags."""
        payload = {
            'title': 'Thai Prawn Curry',
            'time_minutes': 30,
            'price':Decimal('2.50'),
            'tags': [{'name':'thai'}, {'name':'Dinner'}],
        }
        res = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipes = Recipe.objects.filter(user=self.user)
        self.assertEqual(recipes.count(), 1)
        recipe = recipes[0] # assign the first index recipes to the recipe variable
        self.assertEqual(recipe.tags.count(), 2) #count the tag in the  recipe.
        # self.assertEqual(len(payload['tags']), len(recipe.tags)) #checking if the amount of tags that are in the payload is equal to recipe.
        for tag in payload['tags']:
            exists = recipe.tags.filter(name=tag['name'],user=self.user,).exists()
            self.assertTrue(exists)


    def test_create_recipe_with_existing_tags(self):
        """Test that the API can use existing tags."""
        tag_ethio = Tag.objects.create(user=self.user, name='kondo-berebere')
        payload = {
            'title': 'shiro',
            'time_minutes': 30,
            'price': Decimal('4.50'),
            'tags': [{'name':'kondo-berebere'},{'name':'Dinner'}],
        }
        res = self.client.post(RECIPES_URL,payload,format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipes = Recipe.objects.filter(user=self.user)
          # check if it has two tags and one recipe
        self.assertEqual(recipes.count(), 1) #check if it has one recipe
        recipe = recipes[0]
        #checking the name inside the tag.
        self.assertEqual(recipe.tags.count(), 2)
        # self.assertEqual(len(payload['tags']), len(recipe.tags))
        self.assertIn(tag_ethio, recipe.tags.all())
        for tag in payload['tags']:
            exists = recipe.tags.filter(name=tag['name'], user = self.user).exists()
            self.assertTrue(exists)

    def test_create_tag_on_update(self):
        """Test updating a recipe with new tags."""
        recipe = create_recipe(user=self.user) #creating sample recipe.
        payload = {'tags': [{'name': 'Lunch'}]}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        new_tag = Tag.objects.get(user=self.user, name='Lunch') #retrieve the new tag that we created it when we update our recipe.
        self.assertIn(new_tag, recipe.tags.all()) #checking the new_tag from the tags.

    def test_update_recipe_assign_tag(self):
        """Test assigning an existing tag when updating a recipe."""
        tag_fruit = Tag.objects.create(user=self.user, name='orange')
        recipe = create_recipe(user=self.user)
        recipe.tags.add(tag_fruit)

        tag_vege = Tag.objects.create(user=self.user, name='potato')
        payload = {'tags': [{'name': 'potato'}]}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(tag_vege, recipe.tags.all())
        self.assertNotIn(tag_fruit, recipe.tags.all())

    def test_clear_recipe_tag(self):
        '''Test removing all tags from a recipe'''
        tag  = Tag.objects.create(user=self.user, name='Lunch')
        recipe = create_recipe(user=self.user)
        recipe.tags.add(tag)

        payload = {'tags': []} #empty tags
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.tags.count(), 0)

    def test_create_recipe_with_new_ingredient(self):
        """Test creating a recipe with one or more ingredients"""
        payload = {
            'title': 'rice with potatoes',
            'time_minutes': 60,
            'price':Decimal('3.00'),
            'ingredients':[{'name': 'rice'}, {'name': 'potato'}],
        }

        res = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipes = Recipe.objects.filter(user=self.user)
        self.assertEqual(recipes.count(), 1)
        recipe = recipes[0]
        self.assertEqual(recipe.ingredients.count(), 2)

        for ingredient in payload['ingredients']:
            exists = recipe.ingredients.filter(name=ingredient['name'],user=self.user).exists()
            self.assertTrue(exists)

    def test_create_recipe_with_exsting_ingredient(self):
        """Test that we can add an existing ingredient to the recipe"""
        ingredient = Ingredient.objects.create(user=self.user, name='sauce')

        payload = {
            'title': 'rice with potatoes',
            'time_minutes': 60,
            'price':Decimal('3.00'),
            'ingredients':[{'name': 'sauce'}, {'name': 'potato'}, {'name': 'rice'}],
        }
        res = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipes = Recipe.objects.filter(user=self.user)
        self.assertEqual(recipes.count(), 1)
        recipe = recipes[0]
        self.assertEqual(recipe.ingredients.count(), 3)

        self.assertIn(ingredient, recipe.ingredients.all())

        for ingredient in payload['ingredients']:
            exists = recipe.ingredients.filter(name=ingredient['name'], user=self.user).exists()
            self.assertTrue(exists)
    def  test_create_ingredient_on_update(self):
        """Test updating a recipe with new tags"""
        recipe = create_recipe(user=self.user)
        payload = {'ingredients':[{'name': 'Limes'}]}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        new_ingredient = Ingredient.objects.get(user=self.user, name='Limes')
        self.assertIn(new_ingredient, recipe.ingredients.all())

    def test_update_recipe_assign_ingredient(self):
        """Test assigning an existing ingredient when updating a recipe."""
        ingredient = Ingredient.objects.create(user=self.user, name='pepper')
        recipe = create_recipe(user=self.user)
        recipe.ingredients.add(ingredient)

        new_ingredient = Ingredient.objects.create(user=self.user, name='salt')
        payload = {'ingredients':[{'name': 'salt'}]}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(new_ingredient, recipe.ingredients.all())
        self.assertNotIn(ingredient, recipe.ingredients.all())

    def test_clear_recipe_ingredients(self):
        """Test removing all ingredients from a recipe."""

        ingredient = Ingredient.objects.create(user=self.user, name='pepper')
        recipe = create_recipe(user=self.user)
        recipe.ingredients.add(ingredient)

        payload = {'ingredients': []}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.ingredients.count(), 0)

    def test_filter_by_tags(self):
        """Test returning recipes with specific tags"""
        recipe1 = create_recipe(self.user)
        recipe2 = create_recipe(self.user)
        tag1 = Tag.objects.create(user=self.user, name="Vegan")
        tag2 = Tag.objects.create(user=self.user, name="Vegetarian")
        recipe1.tags.add(tag1)
        recipe2.tags.add(tag2)

        recipe3 = create_recipe(user=self.user, title='chekena')
        params = {'tags': f'{tag1.id}, {tag2.id}'}
        res = self.client.get(RECIPES_URL, params)
        #we have to serilize it tho change it into json format
        serializer1 = RecipeSerializer(recipe1)
        serializer2 = RecipeSerializer(recipe2)
        serializer3 = RecipeSerializer(recipe3)
        #check if the data exist in data
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_filter_by_ingredient(self):
        """Test for filtering recipe by specific ingredient."""
        recipe1 = create_recipe(self.user, title="Poshie")
        recipe2 = create_recipe(self.user, title="Beefy")
        ingredient1 = Ingredient.objects.create(user=self.user, name="Bacon")
        ingredient2 = Ingredient.objects.create(user=self.user, name="Salt")
        recipe1.ingredients.add(ingredient1)
        recipe2.ingredients.add(ingredient2)

        recipe3 = create_recipe(self.user, title = "fishy")
        params = {"ingredients":f'{ingredient1.id},{ingredient2.id}'}
        res = self.client.get(RECIPES_URL, params)

        serializer1 = RecipeSerializer(recipe1)
        serializer2 = RecipeSerializer(recipe2)
        serializer3 = RecipeSerializer(recipe3)
            #check if the data exist in data
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)


class ImageUploadTests(TestCase):
    """Test for image upload API."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@gmail.com",
            "password123456789",
        )
        self.client.force_authenticate(self.user)
        self.recipe = create_recipe(user=self.user)

    def tearDown(self):
        # Clean up the media files after each test
        self.recipe.image.delete()


    def test_upload_image(self):
        """Test that we can successfully upload an image to a recipe."""
        url = upload_image_url(self.recipe.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file)
            image_file.seek(0)
            payload = {'image':image_file}
            res = self.client.post(url, payload, format="multipart")

            self.recipe.refresh_from_db()
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertIn("image", res.data)
            self.assertTrue(os.path.exists(self.recipe.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading invalid image"""
        url = upload_image_url(self.recipe.id)
        payload = {'image': 'notanimage'}
        res = self.client.post(url, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)