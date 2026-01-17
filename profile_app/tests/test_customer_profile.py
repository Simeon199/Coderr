from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from auth_app.models import CustomUser
from profile_app.models import CustomerProfile

class CustomerProfileViewTest(APITestCase):
    """
    Test suite for the customer profile list endpoint.
    """

    def setUp(self) -> None:
        # Create an authenticated customer user
        self.customer_user = CustomUser.objects.create_user(
            username="customer_jane",
            password="testpass123",
            first_name="Jane",
            last_name="Doe",
            email="jane@example.com",
            type="customer"
        )

        # Create a CustomerProfile for the user
        self.customer_profile = CustomerProfile.objects.create(
            user=self.customer_user,
            username="customer_jane",
            first_name="Jane",
            last_name="Doe",
            file="profile_picture_customer.jpg",
            uploaded_at="2023-09-15T09:00:00",
            type="customer"
        )

        # Generate a token for the user
        self.token = Token.objects.create(user=self.customer_user)

        self.client = APIClient()

        # Authenticate the client using the token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # Prepare the URL for the view
        self.url = reverse("customer-profile")

    def test_authenticated_user_can_retrieve_profile(self):
        """
        A logged-in user should receive status 200 and the expected JSON payload
        """
        response = self.client.get(self.url, format="json")

        # Status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate response structure
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

        expected_keys = {
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "uploaded_at",
            "type"
        }

        for item in data:
            self.assertIsInstance(item, dict)
            self.assertEqual(set(item.keys()), expected_keys)
            
            # Quick sanity checks
            self.assertEqual(item["user"], self.customer_user.id)
            self.assertEqual(item["username"], "customer_jane")
            self.assertEqual(item["first_name"], "Jane")
            self.assertEqual(item["last_name"], "Doe")
            self.assertEqual(item["file"], "profile_picture_customer.jpg")
            self.assertEqual(item["uploaded_at"], "2023-09-15T09:00:00")
            self.assertEqual(item["type"], "customer")

    def test_unauthenticated_user_cannot_access(self):
        """
        A request without authentication must return 401.
        """
        client = APIClient()
        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)