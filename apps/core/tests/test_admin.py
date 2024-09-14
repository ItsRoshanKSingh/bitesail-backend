"""Test for Django admin modifications"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTest(TestCase):
    """
    Test suite for Django admin interface.

    This class tests the admin interface functionalities including listing,
    editing, and creating users. It ensures that these operations are
    performed correctly from an administrative perspective.
    """

    def setUp(self) -> None:
        """
        Set up test environment with an admin user and a regular user.

        Initializes the test client, creates an admin superuser and a regular
        user, and logs in the admin user to allow authenticated requests.
        """
        self.client = Client()

        # Create an admin superuser
        self.admin_user = get_user_model().objects.create_superuser(
            email="testAdmin@example.com", password="Pass!2024"
        )

        # Create a regular user
        self.user = get_user_model().objects.create_user(
            name="TestUser", email="regularUser@example.com", password="Test@1234"
        )

        # Log in the admin user
        self.client.force_login(self.admin_user)

    def test_user_list(self):
        """
        Test that regular users are listed on the admin interface.

        Sends a GET request to the user list page of the admin interface and
        verifies that the email and name of the regular user are present
        in the response.
        """
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.name)

    def test_edit_user(self):
        """
        Test that the user edit page is accessible.

        Sends a GET request to the user edit page in the admin interface and
        checks that the response status code is 200, indicating that the page
        is accessible for editing.
        """
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_create_user(self):
        """
        Test that the user creation page is accessible.

        Sends a GET request to the user creation page in the admin interface and
        checks that the response status code is 200, indicating that the page
        is accessible for creating new users.
        """
        url = reverse("admin:core_user_add")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
