from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from apps.core import models
from apps.recipe.serializers import TagSerializer

TAGS_URL = reverse("recipe:tag-list")


def detail_url(tag_id):
    return reverse("recipe:tag-detail", args=[tag_id])


def create_user(email="test-user@example.com", password="password"):
    return get_user_model().objects.create(email=email, password=password)


class PublicTagsAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_require_retrive_tags_failed(self):
        response = self.client.get(TAGS_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_auth_require_retrive_tags_successfull(self):
        models.Tag.objects.create(user=self.user, name="vegan")
        models.Tag.objects.create(user=self.user, name="dessert")

        response = self.client.get(TAGS_URL)

        tags = models.Tag.objects.all().order_by("-name")
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_tags_limited_to_users(self):
        tag = models.Tag.objects.create(user=self.user, name="vegan")
        other_user = create_user(email="otherUser@example.com", password="Test@1234")
        models.Tag.objects.create(user=other_user, name="vegan-1")
        models.Tag.objects.create(user=other_user, name="dessert-1")
        response = self.client.get(TAGS_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], tag.name)

    def test_update_tag(self):
        tag = models.Tag.objects.create(user=self.user, name="test-tag")
        url = detail_url(tag.id)
        self.client.patch(url, {"name": "updaed-Tag"})
        tag.refresh_from_db()

        self.assertEqual(tag.name, "updaed-Tag")

    def test_delete_tag(self):
        tag = models.Tag.objects.create(user=self.user, name="testtag")
        url = detail_url(tag.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.Tag.objects.filter(user=self.user).exists())
