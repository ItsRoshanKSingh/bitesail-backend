"""Test for user API"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

# URL for user creation endpoint
CREATE_USER_URL = reverse("user:create")

# URL for token creation endpoint
TOKEN_URL = reverse("user:token")

ME_URL = reverse("user:me")


def create_user(**params):
    """
    Create and return a new user with the given parameters.

    This utility function simplifies the creation of user objects in tests.
    """
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """
    Test suite for the user API endpoints where authentication is not required.

    This class includes tests for creating users, handling errors, and validating
    various conditions related to user creation.
    """

    def setUp(self) -> None:
        """
        Set up the test client for making API requests.

        Initializes the API client which is used to make requests to the API.
        """
        self.client = APIClient()

    def test_create_user_success(self):
        """
        Test successful user creation.

        Sends a POST request with valid user data and verifies that the user
        is created successfully. The response should indicate successful
        creation and the user’s password should be hashed.
        """
        user_payload = {
            "name": "testUser",
            "email": "testUser@example.com",
            "password": "New!2024",
        }

        # Send POST request to create the user
        res = self.client.post(CREATE_USER_URL, user_payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("password", res.data)

        # Verify that the user was created and the password is correctly hashed
        user = get_user_model().objects.get(email=user_payload["email"])
        self.assertTrue(user.check_password(user_payload["password"]))

    def test_create_user_with_existing_email_fail(self):
        """
        Test user creation with an already existing email.

        Attempts to create a new user with an email that is already used by
        an existing user. The response should indicate failure with a
        400 Bad Request status code.
        """
        existing_user_payload = {
            "name": "testUser",
            "email": "testUser@example.com",
            "password": "New!2024",
        }

        # Create a user with the same email
        create_user(**existing_user_payload)

        # Attempt to create another user with the same email
        res = self.client.post(CREATE_USER_URL, existing_user_payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """
        Test user creation with a password that is too short.

        Sends a POST request with a password that is shorter than the minimum
        length requirement. The response should indicate failure with a
        400 Bad Request status code, and no user should be created.
        """
        invalid_password_payload = {
            "name": "testUser",
            "email": "testUser@example.com",
            "password": "New!",
        }

        # Send POST request with a short password
        res = self.client.post(CREATE_USER_URL, invalid_password_payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # Verify that no user was created with the short password
        user_exists = (
            get_user_model()
            .objects.filter(email=invalid_password_payload["email"])
            .exists()
        )
        self.assertFalse(user_exists)

    def test_generate_token_for_valid_credentials(self):
        """
        Test that a token is generated for valid user credentials.
        """

        user_data = {
            "name": "testUser",
            "email": "testUser@example.com",
            "password": "New!2024",
        }

        # Create the user with valid credentials
        create_user(**user_data)

        # Payload for token request
        valid_token_request_data = {
            "email": user_data["email"],
            "password": user_data["password"],
        }

        # Send POST request to obtain token using valid credentials
        response = self.client.post(TOKEN_URL, valid_token_request_data)

        self.assertIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_generate_token_for_invalid_credentials(self):
        """
        Test that a token is not generated for invalid user credentials.
        """

        user_data = {
            "name": "testUser",
            "email": "testUser@example.com",
            "password": "New!2024",
        }

        # Create the user with valid credentials
        create_user(**user_data)

        # Payload for token request with an incorrect email
        invalid_token_request_data = {
            "email": "bad_email@example.com",
            "password": user_data["password"],
        }

        # Send POST request to obtain token using invalid credentials
        response = self.client.post(TOKEN_URL, invalid_token_request_data)

        self.assertNotIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_token_generated_for_blank_password(self):
        """
        Test that a token is not generated when the password is blank.
        """

        # Payload for token request with an invalid email and blank password
        invalid_token_request_data = {
            "email": "bad_email@example.com",
            "password": "",
        }

        # Send POST request to obtain token using invalid credentials
        response = self.client.post(TOKEN_URL, invalid_token_request_data)

        # Assert that the response does not contain a token and the status is 400 Bad Request
        self.assertNotIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """
        Test that retrieving user data without authentication returns 401 Unauthorized.
        """
        # Send GET request to ME_URL without authentication
        res = self.client.get(ME_URL)

        # Assert that the response status code is 401 Unauthorized
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PublicUserApiTest(TestCase):
    """
    Test suite for user-related API endpoints with authentication.
    """

    def setUp(self) -> None:
        """
        Set up a test user and authenticate the client with that user.
        """
        self.user = get_user_model().objects.create_user(
            name="testUser", email="testUser@example.com", password="New!2024"
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user_profile_success(self):
        """
        Test retrieving the authenticated user's profile successfully.

        Sends a GET request to the profile endpoint and verifies that the response status is 200 OK
        and the returned data matches the authenticated user's details.
        """
        response = self.client.get(ME_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "name": self.user.name,
                "email": self.user.email,
            },
        )

    def test_post_to_user_profile_not_allowed(self):
        """
        Test that POST requests to the profile endpoint are not allowed.

        Sends a POST request to the profile endpoint and verifies that the response status is 405 Method Not Allowed.
        """
        response = self.client.post(ME_URL, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile_success(self):
        """
        Test updating the authenticated user's profile successfully.

        Sends a PATCH request with updated user details to the profile endpoint. Then verifies that the user's
        details are updated in the database and the new password is correctly set.
        """
        payload = {
            "name": "updatedUser",
            "email": "updatedUser@example.com",
            "password": "New!2024_",
        }
        response = self.client.patch(ME_URL, payload, format="json")

        # Refresh the user instance from the database
        self.user.refresh_from_db()

        # Verify the user details were updated correctly
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, payload["name"])
        self.assertEqual(self.user.email, payload["email"])
        self.assertTrue(self.user.check_password(payload["password"]))
