from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from reviews_app.models import Review
from offers_app.models import Offer
from profile_app.models import BusinessProfile

User = get_user_model()

class BaseInfoAPITestCase(TestCase):
    """
    Test the public base-info endpoint that returns platform statistics.
    """

    def setUp(self):
        """
        Create a user, two reviews, a business profile and an offer for testing.
        """

        self.client = APIClient()
        self.url = reverse('base-info')
        self.user = User.objects.create_user(username='test_user', password='test_password')
        Review.objects.create(rating=4)
        Review.objects.create(rating=5)
        BusinessProfile.objects.create(user=self.user)
        Offer.objects.create(title="Test Offer")

    def test_base_info_view(self):
        """
        Verify that GET returns correct counts and average rating.
        """
        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['review_count'], 2)
        self.assertEqual(data['average_rating'], 4.5)
        self.assertEqual(data['business_profile_count'], 2)
        self.assertEqual(data['offer_count'], 1)