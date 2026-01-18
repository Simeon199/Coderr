from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .test_generic_user_profile import ProfileTests

class BusinessProfileTests(ProfileTests):
    """
    Test the business profile endpoint that returns a list of business users.
    """
    def setUp(self):
        super().setUp()
        # Update the user type to business
        self.user.type = "business"
        self.user.save()

        # Update the BusinessProfile for the user
        self.business_profile = self.profile
        self.business_profile.file = "profile_picture.jpg"
        self.business_profile.location = "Berlin"
        self.business_profile.tel = "123456789"
        self.business_profile.description = "Business description"
        self.business_profile.working_hours = "9-17"
        self.business_profile.save()

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
            self.assertEqual(item["user"], self.user.id)
            self.assertEqual(item["username"], "test_user")
            self.assertEqual(item["first_name"], "Test")
            self.assertEqual(item["last_name"], "User")
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