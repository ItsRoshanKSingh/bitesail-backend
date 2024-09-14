"""Tests for Models"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


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
