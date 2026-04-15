from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from auth_app.models import CustomUser
from profile_app.models import BusinessProfile, CustomerProfile


class GuestLoginTest(APITestCase):
    """
    Verify that the guest users seeded by the data migration
    (auth_app/migrations/0008_create_guest_users.py) can log in via the
    standard login endpoint, as required by the frontend's guest login flow.
    """

    def setUp(self):
        self.url = reverse("login")

    def test_customer_guest_can_log_in(self):
        """
        The customer guest user (andrey) must authenticate successfully
        and receive the expected token response.
        """

        response = self.client.post(
            self.url,
            {"username": "andrey", "password": "asdasd"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["username"], "andrey")
        user = CustomUser.objects.get(username="andrey")
        self.assertEqual(response.data["user_id"], user.id)
        self.assertEqual(response.data["token"], Token.objects.get(user=user).key)

    def test_business_guest_can_log_in(self):
        """
        The business guest user (kevin) must authenticate successfully
        and receive the expected token response.
        """

        response = self.client.post(
            self.url,
            {"username": "kevin", "password": "asdasd24"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["username"], "kevin")
        user = CustomUser.objects.get(username="kevin")
        self.assertEqual(response.data["user_id"], user.id)
        self.assertEqual(response.data["token"], Token.objects.get(user=user).key)

    def test_customer_guest_has_correct_type_and_profile(self):
        """
        The customer guest user must have type 'customer' and a matching
        CustomerProfile so downstream endpoints work out of the box.
        """

        user = CustomUser.objects.get(username="andrey")
        self.assertEqual(user.type, "customer")
        self.assertTrue(CustomerProfile.objects.filter(user=user).exists())
        self.assertFalse(BusinessProfile.objects.filter(user=user).exists())

    def test_business_guest_has_correct_type_and_profile(self):
        """
        The business guest user must have type 'business' and a matching
        BusinessProfile so downstream endpoints work out of the box.
        """

        user = CustomUser.objects.get(username="kevin")
        self.assertEqual(user.type, "business")
        self.assertTrue(BusinessProfile.objects.filter(user=user).exists())
        self.assertFalse(CustomerProfile.objects.filter(user=user).exists())

    def test_guest_login_with_wrong_password_fails(self):
        """
        A wrong password for a guest username must not unlock the account.
        """

        response = self.client.post(
            self.url,
            {"username": "andrey", "password": "wrong"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
