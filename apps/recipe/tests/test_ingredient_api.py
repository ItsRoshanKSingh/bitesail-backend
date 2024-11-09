from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from apps.core.models import Ingredient
from ..serializers import IngredientSerializer


INGREDIENT_URL = reverse("recipe:ingredient-list")


def create_user(email="test@example.com", password="Test@1234"):
    return get_user_model().objects.create(email=email, password=password)


def detail_url(ingredient_id):
    return reverse("recipe:ingredient-detail", args=[ingredient_id])


class PublicIngredientAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required_ingredient(self):
        response = self.client.get(INGREDIENT_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_ingredient(self):
        Ingredient.objects.create(user=self.user, name="Tomato")
        Ingredient.objects.create(user=self.user, name="Potato")

        response = self.client.get(INGREDIENT_URL)

        ingredient = Ingredient.objects.all().order_by("-name")
        serializer = IngredientSerializer(ingredient, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_ingredient_limited_user(self):
        ingredient = Ingredient.objects.create(user=self.user, name="Tomato")

        Ingredient.objects.create(
            user=create_user(email="New@example.com"), name="Onion"
        )

        response = self.client.get(INGREDIENT_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], ingredient.name)
        self.assertEqual(response.data[0]["id"], ingredient.id)

    def test_update_ingredient(self):
        ingredient = Ingredient.objects.create(user=self.user, name="Roma Tomato")

        url = detail_url(ingredient.id)
        response = self.client.patch(url, {"name": "white Potato"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "white Potato")

        in_res = Ingredient.objects.filter(user=self.user)
        self.assertEqual(in_res[0].name, "white Potato")

    def test_delete_ingredient(self):
        ingredient = Ingredient.objects.create(user=self.user, name="Roma Tomato")
        url = detail_url(ingredient.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        ingredient_res = Ingredient.objects.filter(user=self.user)
        self.assertFalse(ingredient_res.exists())
