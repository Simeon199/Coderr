from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from auth_app.models import CustomUser
from profile_app.models import BusinessProfile, CustomerProfile

class ProfileTests(APITestCase):
    """
    Base test class for testing profile patch logic.
    """

    def setUp(self):
        """
        Create an authenticated business user with profile, token and API client.
        """

        self.user = CustomUser.objects.create_user(
            username="test_user",
            password="secret123",
            first_name="Test",
            last_name="User",
            email="test@example.com",
            type="business" 
        )
        self.token = Token.objects.create(user=self.user)
        if self.user.type == "business":
            self.profile = BusinessProfile.objects.create(
                user=self.user,
                location="",
                tel="",
                description="",
                working_hours=""
            )
        else:
            self.profile = CustomerProfile.objects.create(
                user=self.user
            )
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_update_profile_as_account_admin(self):
        """
        Verify that the profile owner can patch their own profile fields.
        """

        url = reverse('user-profile', kwargs={'user': self.user.pk})
        self.client.force_authenticate(user=self.user)
        data = {}
        if self.user.type == "business":
            data["location"] = "New York"
        else:
            data["first_name"] = "Updated"
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if self.user.type == "business":
            self.assertEqual(response.data["location"], "New York")
        else:
            self.assertEqual(response.data["first_name"], "Updated")

    def test_update_profile_as_non_account_admin(self):
        """
        Verify that a user cannot patch another user's profile (403).
        """

        other_user = CustomUser.objects.create_user(
            username="other_user",
            password="secret123",
            first_name="Other",
            last_name="User",
            email="other@example.com",
            type="business"  
        )
        BusinessProfile.objects.create(
            user=other_user,
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
        """
        Verify that an unauthenticated user cannot patch a profile (401).
        """

        unauth_client = APIClient()
        url = reverse('user-profile', kwargs={'user': self.user.pk})
        data = {
            "location": "New York"
        }
        response = unauth_client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_own_profile_as_authenticated_user(self):
        """
        Test that an authenticated user can access their own profile.
        """

        url = reverse('user-profile', kwargs={'user': self.user.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertIn('username', response.data)
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)
        self.assertIn('file', response.data)
        self.assertIn('type', response.data)

        if self.user.type == 'business':
            self.assertIn('location', response.data)
            self.assertIn('tel', response.data)
            self.assertIn('description', response.data)
            self.assertIn('working_hours', response.data)

        self.assertEqual(response.data["user"], self.user.pk)
        self.assertEqual(response.data["username"], self.user.username)
        self.assertEqual(response.data["first_name"], self.user.first_name)
        self.assertEqual(response.data["last_name"], self.user.last_name)
        self.assertEqual(response.data["type"], self.user.type)

    def test_get_own_profile_unauthenticated(self):
        """
        Test that an unauthenticated user cannot access his profile.
        """
        
        unauth_client = APIClient()
        url = reverse('user-profile', kwargs={'user': self.user.pk})
        response = unauth_client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_fields_not_null(self):
        """
        Test that required fields are not null and are set to an empty string if no value is
        assigned.
        """
        
        url = reverse('user-profile', kwargs={'user': self.user.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get("first_name"))
        self.assertIsNotNone(response.data.get("last_name"))
        self.assertEqual(response.data.get("first_name"),self.user.first_name if self.user.first_name else "")
        self.assertEqual(response.data.get("last_name"), self.user.last_name if self.user.last_name else "")
        if self.user.type == "business":
            self.assertIsNotNone(response.data.get("location"))
            self.assertIsNotNone(response.data.get("tel"))
            self.assertIsNotNone(response.data.get("description"))
            self.assertIsNotNone(response.data.get("working_hours"))
            self.assertEqual(response.data.get("location"), self.profile.location if self.profile.location else "")
            self.assertEqual(response.data.get("tel"), self.profile.tel if self.profile.tel else "")
            self.assertEqual(response.data.get("description"), self.profile.description if self.profile.description else "")
            self.assertEqual(response.data.get("working_hours"), self.profile.working_hours if self.profile.working_hours else "")