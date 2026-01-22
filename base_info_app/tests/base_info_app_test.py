from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from reviews_app.models import Review
from offers_app.models import Offer
from profile_app.models import BusinessProfile

User = get_user_model()
# from base_info_app.models import BaseInfo
# from base_info_app.api.serializers import BaseInfoSerializer

class BaseInfoAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('base-info')

        # Create a user for the BusinessProfile
        self.user = User.objects.create_user(username='test_user', password='test_password')

        # Create test data
        Review.objects.create(rating=4)
        Review.objects.create(rating=5)
        BusinessProfile.objects.create(user=self.user, username="test_business")
        Offer.objects.create(title="Test Offer")

    def test_base_info_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify response data
        data = response.data
        self.assertEqual(data['review_count'], 2)
        self.assertEqual(data['average_rating'], 4.5)
        self.assertEqual(data['business_profile_count'], 1)
        self.assertEqual(data['offer_count'], 1)

    #     self.client = APIClient()
    #     self.base_info = BaseInfo.objects.create(
    #         review_count = 10,
    #         average_rating = 4.5,
    #         business_profile_count = 5,
    #         offer_count = 3
    #     )
    #     self.url = reverse('base-info')

    # def test_base_info_serializer(self):
    #     serializer = BaseInfoSerializer(isinstance=self.base_info)
    #     data = serializer.data
    #     self.assertEqual(data['review_count'], 10)
    #     self.assertEqual(data['average_rating'], 4.5)
    #     self.assertEqual(data['business_profile_count'], 5)
    #     self.assertEqual(data['offer_count'], 20)

    # def test_base_info_list_view(self):
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 1)
    #     self.assertEqual(response.data[0]['review_count'], 10)