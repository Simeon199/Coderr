from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from auth_app.models import CustomUser
from profile_app.models import CustomerProfile
from .test_generic_user_profile import ProfileTests

class CustomerProfileViewTest(ProfileTests):
    """
    Test suite for the customer profile list endpoint.
    """

    def setUp(self) -> None:

        """
        Create an authenticated customer user with profile, token and API client.
        """
        self.user = CustomUser.objects.create_user(
            username="test_user",
            password="secret123",
            first_name="Test",
            last_name="User",
            email="test@example.com",
            type="customer"
        )

        self.token = Token.objects.create(user=self.user)
        self.profile = CustomerProfile.objects.create(
            user=self.user
        )
        self.customer_profile = self.profile
        self.user.file = "profile_picture.jpg"
        self.user.save()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.url = reverse("customer-profile")

    def test_authenticated_user_can_retrieve_profile(self):
        """
        A logged-in user should receive status 200 and the expected JSON payload.
        """
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

        expected_keys = {
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "type"
        }

        for item in data:
            self.assertIsInstance(item, dict)
            self.assertEqual(set(item.keys()), expected_keys)
            self.assertEqual(item["user"], self.user.id)
            self.assertEqual(item["username"], "test_user")
            self.assertEqual(item["first_name"], "Test")
            self.assertEqual(item["last_name"], "User")
            self.assertEqual(item["file"], "profile_picture.jpg")

    def test_unauthenticated_user_cannot_access(self):
        """
        A request without authentication must return 401.
        """
        client = APIClient()
        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)