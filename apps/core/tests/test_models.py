"""Tests for Models"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from decimal import Decimal
from apps.core import models


def create_user(email="dummy-user@example.com", password="Test@1234"):
    return get_user_model().objects.create_user(email=email, password=password)


class ModelTests(TestCase):
    """Test Models."""

    def test_create_user_with_email_successfull(self):
        """Test create a user with email successfull"""

        email = "test@example.com"
        password = "Pass!2024"

        """
        create_user: is responsible for creating and saving a new user instance.
                     It abstracts the process of creating a user object, handling
                     common tasks like setting hashed passwords instead of plain text passwords.
        """
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_superuser(self):
        """Test creating a superuser"""

        user = get_user_model().objects.create_superuser(
            email="superuser@example.com", password="IamSuper!"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test creating recipe successfull"""

        user = get_user_model().objects.create_user(
            email="test@example.com", password="Test@1234"
        )

        recipe = models.Recipe.objects.create(
            user=user,
            title="Test Recipe",
            time_minute=10,
            price=Decimal("10.12"),
            description="Sample Recipe Description",
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        user = create_user()
        tag = models.Tag.objects.create(user=user, name="tag1")
        self.assertEqual(str(tag), tag.name)

    def test_create_ingredient(self):
        user = create_user()
        ingredient = models.Ingredient.objects.create(user=user, name="Tomato")
        self.assertEqual(str(ingredient), "Tomato")
