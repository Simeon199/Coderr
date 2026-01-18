from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from auth_app.models import CustomUser
from profile_app.models import BusinessProfile, CustomerProfile

class ProfilePatchTests(APITestCase):
    """
    Base test class for testing profile patch logic.
    """
    def setUp(self):
        # Create an authenticated user
        self.user = CustomUser.objects.create_user(
            username="test_user",
            password="secret123",
            first_name="Test",
            last_name="User",
            email="test@example.com",
            type="business"  # Default type; can be overridden in child classes
        )

        # Generate a token for the user
        self.token = Token.objects.create(user=self.user)

        # Create a profile for the user
        if self.user.type == "business":
            self.profile = BusinessProfile.objects.create(
                user=self.user,
                username=self.user.username,
                first_name=self.user.first_name,
                last_name=self.user.last_name,
                file="",
                location="",
                tel="",
                description="",
                working_hours=""
            )
        else:
            self.profile = CustomerProfile.objects.create(
                user=self.user,
                username=self.user.username,
                first_name=self.user.first_name,
                last_name=self.user.last_name,
                file=""
            )

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_update_profile_as_account_admin(self):
        url = reverse('user-profile', kwargs={'user': self.user.pk})
        self.client.force_authenticate(user=self.user)
        data = {}
        
        # For business profiles, test updating location
        if self.user.type == "business":
            data["location"] = "New York"
        else:
            # For customer profiles, test updating first_name
            data["first_name"] = "Updated"
        
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        if self.user.type == "business":
            self.assertEqual(response.data["location"], "New York")
        else:
            self.assertEqual(response.data["first_name"], "Updated")

    def test_update_profile_as_non_account_admin(self):
        # Create another user to simulate a non-account admin
        other_user = CustomUser.objects.create_user(
            username="other_user",
            password="secret123",
            first_name="Other",
            last_name="User",
            email="other@example.com",
            type="business"  # Default type; can be overridden in child classes
        )

        # Create a profile for the other user
        BusinessProfile.objects.create(
            user=other_user,
            username=other_user.username,
            first_name=other_user.first_name,
            last_name=other_user.last_name,
            file="",
            location="",
            tel="",
            description="",
            working_hours=""
        )

        url = reverse('user-profile', kwargs={'user': other_user.pk})
        self.client.force_authenticate(user=self.user)
        data = {
            "location": "New York"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_profile_as_non_authenticated(self):
        # Create a fresh unauthenticated client
        unauth_client = APIClient()
        url = reverse('user-profile', kwargs={'user': self.user.pk})
        data = {
            "location": "New York"
        }
        response = unauth_client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)