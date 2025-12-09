from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch

class RegistrationAPITest(APITestCase):
    """
    Test the user registration endpoint.
    """
    
    def setUp(self):
        self.url = reverse("registration")

    def test_registration_successfull(self):
        """
        Ensure that a valid POST creates a user and returns the expected payload.
        """
        data = {
            "fullname": "Example Username",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword"
        }

        response = self.client.post(self.url, data, format="json")

        # 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Token should be a non-empty string
        self.assertIn("token", response.data)
        self.assertTrue(isinstance(response.data["token"], str))
        self.assertGreater(len(response.data["token"]), 0)

        # Expected fields
        expected_keys = {"token", "fullname", "email", "user_id"}
        self.assertEqual(set(response.data.keys()), expected_keys)

        # Verify values match what was sent (except token & user_id)
        self.assertEqual(response.data["fullname"], data["fullname"])
        self.assertEqual(response.data["email"], data["email"])

    def test_registration_missing_field(self):
        """
        POST without a required field should return 400.
        """
        incomplete_data = {
            "fullname": "Example Username",
            # email omitted
            "password": "examplePassword",
            "repeated_password": "examplePassword"
        }

        response = self.client.post(self.url, incomplete_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_internal_error(self):
        """
        Simulate an internal error (e.g., database failure) and assert 500.
        """

        with patch("auth_app.api.serializers.RegistrationSerializer.is_valid") as mocked_is_valid:
            mocked_is_valid.side_effect = Exception("Simulated DB failure")

            data = {
                "fullname": "Example Username",
                "email": "example@mail.de",
                "password": "examplePassword",
                "repeated_password": "examplePassword"
            }

            response = self.client.post(self.url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)