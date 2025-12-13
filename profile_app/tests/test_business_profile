import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from views import BusinessListView

User = get_user_model

class BusinessProfileTests(APITestCase):
    """
    Test the business profile endpoint that returns a list of business users.
    """
    @classmethod
    def setUpTestData(cls):
        # Create an authenticated business user
        cls.business_user = User.objects.create_user(
            username="max_business",
            password="secret123",
            first_name="Max",
            last_name="Mustermann",
            email="max@example.com",
            file="profile_picture.jpg",
            location="Berlin",
            tel="123456789",
            description="Business description",
            working_hours="9-17",
            type="business",
        )
        cls.client = APIClient()
        # authenticate the client - DRF's Token or Session auth can be used
        cls.client.force_authenticate(user=cls.business_user)

    def test_authenticated_user_receives_expected_payload(self):
        url = reverse("business-profile")
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data))

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
            self.assertEqual(item["user"], self.__class__s.business_user.id)
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

    def test_internal_server_error(self):
        """
        Simulate an internal server error and verify 500.
        """
        original_get = BusinessListView.get

        def _error(*args, **kwargs):
            raise RuntimeError("simulated failure")

        BusinessListView.get = _error
        try: 
            response = self.client.get(reverse("business-profile"), format="json")
            self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            # restore the original implementation so other tests keep working
            BusinessListView.get = original_get 