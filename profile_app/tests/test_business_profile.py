from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APIClient
from upload_app.models import FileUpload
from .test_generic_user_profile import ProfileTests

class BusinessProfileTests(ProfileTests):
    """
    Test the business profile endpoint that returns a list of business users.
    """

    def setUp(self):
        """Extend the parent setUp with business-specific profile data."""
        super().setUp()
        self.user.type = "business"
        self.user.save()

        self.business_profile = self.profile
        self.business_profile.location = "Berlin"
        self.business_profile.tel = "123456789"
        self.business_profile.description = "Business description"
        self.business_profile.working_hours = "9-17"
        self.business_profile.save()

        uploaded_file = SimpleUploadedFile("profile_picture.jpg", b"file_content", content_type="image/jpeg")
        self.file_upload = FileUpload.objects.create(file=uploaded_file)
        self.user.file = self.file_upload
        self.user.save()

    def test_authenticated_user_receives_expected_payload(self):
        """
        Verify that an authenticated user receives all expected business profile fields.
        """

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

        item = next((entry for entry in data if entry["user"] == self.user.id), None)
        self.assertIsNotNone(item, "test_user's business profile missing from response")
        self.assertEqual(set(item.keys()), expected_keys)
        self.assertEqual(item["username"], "test_user")
        self.assertEqual(item["first_name"], "Test")
        self.assertEqual(item["last_name"], "User")
        self.assertEqual(item["file"], self.file_upload.file.url)
        self.assertEqual(item["location"], "Berlin")
        self.assertEqual(item["tel"], "123456789")
        self.assertEqual(item["description"], "Business description")
        self.assertEqual(item["working_hours"], "9-17")
        self.assertEqual(item["type"], "business")

    def test_unauthenticated_user_gets_401(self):
        """
        Unauthenticated requests should be rejected with 401.
        """
        
        unauth_client = APIClient()
        response = unauth_client.get(reverse("business-profile"), format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)