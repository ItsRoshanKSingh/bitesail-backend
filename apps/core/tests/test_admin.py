"""Test for django admin modification"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTest(TestCase):
    """Test for django admin"""

    def setUp(self) -> None:
        """Create user and Client"""

        self.client = Client()

        # Admin User
        self.admin_user = get_user_model().objects.create_superuser(
            email="testAdmin@example.com", password="Pass!2024"
        )

        # Regular_User
        self.user = get_user_model().objects.create_user(
            name="TestUser", email="regularUser@example.com", password="Test@1234"
        )

        self.client.force_login(self.admin_user)

    def test_user_list(self):
        """Test regular user are listed on admin interface page"""

        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.name)

    def test_edit_user(self):
        """Edit user successfull"""
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_create_user_test(self):
        """Test createing user work successfully"""
        url = reverse("admin:core_user_add")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
