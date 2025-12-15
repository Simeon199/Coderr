import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch

User = get_user_model()

class CustomerProfileViewTest(APITestCase):
    """
    Test suite for the customer profile list endpoint.
    """

    def setUp(self) -> None:
        # Create a user that will act as an authenticated customer
        self.customer_user = User.objects.create_user(
            username="customer_jane",
            password="testpass123",
            first_name="Jane",
            last_name="Doe",
            email="jane@example.com"
        )

        self.customer_user.profile.picture.name = "profile_picture_customer.jpg"
        self.customer_user.profile.uploaded_at = "2023-09-15T09:00:00"
        self.customer_user.profile.type = "customer"
        self.customer_user.profile.save()

        # Create a second user that will *not* be authenticated in the tests

        User.objects.create_user(
            username="other_user",
            password="irrelevant",
            first_name="John",
            last_name="Smith",
        )

        # Prepare the URL for the view
        self.url = reverse("customer-profile")

    def test_authenticated_user_can_retrieve_profile(self):
        """
        A logged-in user should receive status 200 and the expected JSON payload
        """
        client = APIClient()
        client.login(username="customer_jane", password="testpass123")

        response=client.get(self.url)

        # status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Expected JSON structure (order of keys is irrelevant)
        expected_payload = [
            {
                "user": self.customer_user.pk,
                "username": "customer_jane",
                "first_name": "Jane",
                "last_name": "Doe",
                "file": "profile_picture_customer.jpg",
                "uploaded_at": "2023-09-15T09:00:00",
                "type": "customer",
            }
        ]

        # Compare payload
        self.assertEqual(response.json(), expected_payload)

    def test_unauthenticated_user_cannot_access(self):
        """
        A request without authentication must return 401.
        """
        client = APIClient()
        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_internal_server_error_handling(self):
        """
        Simulate an internal error (e.g. database outage) and ensure the view returns 500.
        """
        client = APIClient()
        client.login(username="customer_jane", password="testpass123")

        # Patch the serializer to raise an exception
        with patch(
            "profile_app.api.views.CustomerSerializer",
            side_effect=Exception("simulated failure")
        ):
            response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
