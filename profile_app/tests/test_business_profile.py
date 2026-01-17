from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from auth_app.models import CustomUser
from profile_app.models import BusinessProfile

class BusinessProfileTests(APITestCase):
    """
    Test the business profile endpoint that returns a list of business users.
    """
    def setUp(self):
        # Create an authenticated business user
        self.business_user = CustomUser.objects.create_user(
            username="max_business",
            password="secret123",
            first_name="Max",
            last_name="Mustermann",
            email="max@example.com",
            type="business"
        )

        # Create a BusinessProfile for the user
        self.business_profile = BusinessProfile.objects.create(
            user=self.business_user,
            username="max_business",
            first_name="Max",
            last_name="Mustermann",
            file="profile_picture.jpg",
            location="Berlin",
            tel="123456789",
            description="Business description",
            working_hours="9-17"
        )

        # Generate a token for the user
        self.token = Token.objects.create(user=self.business_user)

        self.client = APIClient()

        # Authenticate the client using the token 
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_authenticated_user_receives_expected_payload(self):
        url = reverse("business-profile")
        response = self.client.get(url, format="json")

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
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
        }

        for item in data:
            self.assertIsInstance(item, dict)
            self.assertEqual(set(item.keys()), expected_keys)

            # Quick sanity checks
            self.assertEqual(item["user"], self.business_user.id)
            self.assertEqual(item["username"], "max_business")
            self.assertEqual(item["first_name"], "Max")
            self.assertEqual(item["last_name"], "Mustermann")
            self.assertEqual(item["file"], "profile_picture.jpg")
            self.assertEqual(item["location"], "Berlin")
            self.assertEqual(item["tel"], "123456789")
            self.assertEqual(item["description"], "Business description")
            self.assertEqual(item["working_hours"], "9-17")
            self.assertEqual(item["type"], "business")

    def test_unauthenticated_user_gets_401(self):
        """
        Unauthenticated requests should be rejected with 401
        """
        # use a fresh client that is not authenticated
        unauth_client = APIClient()
        response = unauth_client.get(reverse("business-profile"), format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)