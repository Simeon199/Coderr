from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

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

        User = get_user_model()
        user = User.objects.create_user(
            username="exampleUsername",
            password="examplePassword",
            type="customer"
        )
        
        Token.objects.create(user=user)
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify response data structure
        self.assertIn("token", response.data)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)
        self.assertIn("user_id", response.data)
        self.assertEqual(response.data["username"], "exampleUsername")

    def test_login_missing_field(self):
        # Missing password field
        data = {"username": "exampleUsername"}
        response = self.client.post(self.url, data, format="json")

        # Expecting a 400 BAD Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # The error message should point to the missing field
        self.assertIn("password", response.data)

        # Missing username field
        data = {"password": "examplePassword"}
        response = self.client.post(self.url, data, format="json")

        # Expecting a 400 BAD Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # The error message should point to the missing field
        self.assertIn("username", response.data)

    def test_login_invalid_password_or_username(self):
        User = get_user_model()
        User.objects.create_user(
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
        self.assertIn("error", response1.data)

        # Wrong username
        data_wrong_user = {
            "username": "unknownUser",
            "password": "anyPassword"
        }
        response2 = self.client.post(self.url, data_wrong_user, format="json")
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response2.data)