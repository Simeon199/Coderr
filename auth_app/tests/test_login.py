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
        """
        Set up the login URL used by all test methods.
        """
        self.url = reverse("login")

    def test_login_successfull(self):
        """
        Verify that valid credentials return a 200 response with token, username, email and user_id.
        """
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
        self.assertIn("token", response.data)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)
        self.assertIn("user_id", response.data)
        self.assertEqual(response.data["username"], "exampleUsername")

    def test_login_missing_field(self):
        """
        Verify that omitting username or password returns a 400 error.
        """
        data = {"username": "exampleUsername"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)
        data = {"password": "examplePassword"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)

    def test_login_invalid_password_or_username(self):
        """
        Verify that a wrong password or unknown username returns a 400 error.
        """
        User = get_user_model()
        User.objects.create_user(
            username="exampleUsername",
            password="correctPassword"
        )
        data_wrong_password = {
            "username": "exampleUsername", 
            "password": "wrong"
        }
        response1 = self.client.post(self.url, data_wrong_password, format="json")
        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response1.data)
        data_wrong_user = {
            "username": "unknownUser",
            "password": "anyPassword"
        }
        response2 = self.client.post(self.url, data_wrong_user, format="json")
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response2.data)