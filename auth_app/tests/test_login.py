from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from unittest import mock

class LoginAPITest(APITestCase):
    """
    Test the user login endpoint
    """
    def setUp(self):
        self.url = reverse("login")

    def test_login_successfull(self):
        data = {
            "username": "exampleUsername",
            "password": "examplePassword"
        }

        # Create a user first (or use a fixture)
        User = get_user_model()
        User.objects.create_user(
            username="exampleUsername",
            password="examplePassword"
        )
        
        response = self.client.post(self.url, data, format="json")

        # Status code should be 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_missing_field(self):
        # Missing password field
        data = {"username": "exampleUsername"}
        response = self.client.post(self.url, data, format="json")

        # Expecting a 400 BAD Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # The error message should point to the missing field
        self.assertIn("password", response.data)

    def test_login_invalid_password_or_username(self):
        User = get_user_model()
        User.obects.create_user(
            username="exampleUsername",
            password="correctPassword"
        )

        # Wrong password
        data_wrong_password = {
            "username": "exampleUsername", 
            "password": "wrong"
        }
        response1 = self.client.post(self.url, data_wrong_password, format="json")
        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response1.data)

        # Wrong username
        data_wrong_user = {
            "username": "unknownUser",
            "password": "anyPassword"
        }
        response2 = self.client.post(self.url, data_wrong_user, format="json")
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response2.data)
        

    def test_login_internal_error(self):
        # Simulate an unexpected exception in the view (e.g, DB outage).
        # Patch the authentication backend to raise a generic Exception.
        with mock.patch(
            "auth_app.views.CustomAuthView.authenticate",
            side_effect=Exception("DB connection lost")
        ):
            data = {
                "username": "exampleUsername",
                "password": "anyPassword"
            } 
            response = self.client.post(self.url, data, format="json")

        # Expect a 500 Internal Server Error
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("detail", response.data) 