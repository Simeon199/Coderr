from django.urls import reverse
from rest_framework.test import APITestCase

class LoginAPITest(APITestCase):
    """
    Test the user login endpoint
    """
    def setUp(self):
        self.url = reverse("login")

    def test_login_successfull(self):
        pass

    def test_login_missing_field(self):
        pass

    def test_login_invalid_password_or_username(self):
        pass

    def test_login_internal_error(self):
        pass