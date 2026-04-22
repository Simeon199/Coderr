from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from auth_app.models import CustomUser
from profile_app.models import CustomerProfile
from upload_app.models import FileUpload
from .test_generic_user_profile import ProfileTests

class CustomerProfileViewTest(ProfileTests):
    """
    Test suite for the customer profile list endpoint.
    """

    def setUp(self) -> None:

        """
        Create an authenticated customer user with profile, token and API client.
        """
        self.user = CustomUser.objects.create_user(
            username="test_user",
            password="secret123",
            first_name="Test",
            last_name="User",
            email="test@example.com",
            type="customer"
        )

        self.token = Token.objects.create(user=self.user)
        self.profile = CustomerProfile.objects.create(
            user=self.user
        )
        self.customer_profile = self.profile
        uploaded_file = SimpleUploadedFile("profile_picture.jpg", b"file_content", content_type="image/jpeg")
        self.file_upload = FileUpload.objects.create(file=uploaded_file)
        self.user.file = self.file_upload
        self.user.save()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.url = reverse("customer-profile")

    def test_authenticated_user_can_retrieve_profile(self):
        """
        A logged-in user should receive status 200 and the expected JSON payload.
        """
        response = self.client.get(self.url, format="json")
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
            "type"
        }

        item = next((entry for entry in data if entry["user"] == self.user.id), None)
        self.assertIsNotNone(item, "test_user's customer profile missing from response")
        self.assertEqual(set(item.keys()), expected_keys)
        self.assertEqual(item["username"], "test_user")
        self.assertEqual(item["first_name"], "Test")
        self.assertEqual(item["last_name"], "User")
        self.assertEqual(item["file"], f"http://testserver{self.file_upload.file.url}")

    def test_unauthenticated_user_cannot_access(self):
        """
        A request without authentication must return 401.
        """
        client = APIClient()
        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)