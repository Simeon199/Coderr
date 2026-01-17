from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

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
            "username": "ExampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "customer"
        }

        response = self.client.post(self.url, data, format="json")

        # 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Token should be a non-empty string
        self.assertIn("token", response.data)
        self.assertTrue(isinstance(response.data["token"], str))
        self.assertGreater(len(response.data["token"]), 0)

        # Expected fields
        expected_keys = {"token", "username", "email", "user_id"}
        self.assertEqual(set(response.data.keys()), expected_keys)

        # Verify values match what was sent (except token & user_id)
        self.assertEqual(response.data["username"], data["username"])
        self.assertEqual(response.data["email"], data["email"])

    def test_registration_missing_field(self):
        """
        POST without a required field should return 400.
        """

        # Test for missing email
        incomplete_data = {
            "username": "ExampleUsername",
            "password": "examplePassword",
            "repeated_password": "examplePassword"
        }

        response = self.client.post(self.url, incomplete_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test for missing 'type' field
        incomplete_data_without_type = {
            "username": "ExampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword"
        }

        response = self.client.post(self.url, incomplete_data_without_type, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test for missing username
        incomplete_data_without_username = {
            "email": "random@mail.com",
            "password": "ExamplePassword",
            "repeated_password": "ExamplePassword"
        }

        response = self.client.post(self.url, incomplete_data_without_username, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_password_missmatch(self):
        """
        POST with mismatched passwords should return 400.
        """
        data = {
            "username": "ExampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "differentPassword", # Mismatched password
            "type": "customer"
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_registration_email_and_username_uniqueness(self):
        """
        POST with duplicate email or username should return 400.
        """
        # Create a user first
        initial_data = {
            "username": "InitialUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "customer"
        }

        initial_response = self.client.post(self.url, initial_data, format='json')
        self.assertEqual(initial_response.status_code, status.HTTP_201_CREATED)

        # Try to create antother user with the same email 
        duplicate_email_data = {
            "username": "ExampleUsername",
            "email": "example@mail.de", # Duplicate email
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "customer"
        }

        response = self.client.post(self.url, duplicate_email_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

        # Try to create another user with the same username
        duplicate_username_data = {
            "username": "InitialUsername", # Duplicate username
            "email": "different@example.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "customer"
        }

        response = self.client.post(self.url, duplicate_username_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)