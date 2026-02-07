from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from reviews_app.models import Review
from profile_app.models import BusinessProfile, CustomerProfile
from auth_app.models import CustomUser

class ReviewAPITestCase(APITestCase):
    """
    Test suite covering CRUD operations, permissions and validation for the reviews API.
    """

    def setUp(self):
        """
        Create customer and business users, profiles and sample reviews for testing.
        """
        self.customer_user = CustomUser.objects.create_user(
            username="testcustomer",
            password="testpass123",
            type='customer'
        )

        self.business_user = CustomUser.objects.create_user(
            username="testbusiness",
            password="testpass123",
            type='business'
        )

        self.business_profile = BusinessProfile.objects.create(
            user=self.business_user,
            location="Test Location",
            tel="123456789",
            description="Test Description",
            working_hours="9 AM - 5 PM"
        )

        self.customer_profile = CustomerProfile.objects.create(
            user=self.customer_user
        )

        self.customer_user_2 = CustomUser.objects.create_user(
            username="testcustomer2",
            password="testpass123",
            type='customer'
        )
        self.customer_profile_2 = CustomerProfile.objects.create(
            user=self.customer_user_2
        )

        self.review = Review.objects.create(
            business_user=self.business_profile,
            reviewer=self.customer_profile,
            rating=4,
            description="Sehr professioneller Service"
        )

        Review.objects.create(
            business_user=self.business_profile,
            reviewer=self.customer_profile_2,
            rating=5,
            description="Top Qualität und schnelle Lieferung!"
        )

    def test_get_reviews_structure(self):
        """
        Verify that each review in the list contains all required fields with correct types.
        """
        url = reverse('review-list')
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        required_fields = {"id", "business_user", "reviewer", "rating", "description", "created_at", "updated_at"}

        for review in response.data:
            self.assertTrue(required_fields.issubset(review.keys()))
            self.assertIsInstance(review["id"], int)
            self.assertIsInstance(review["business_user"], int)
            self.assertIsInstance(review["reviewer"], int)
            self.assertIsInstance(review["rating"], int)
            self.assertIsInstance(review["description"], str)
            self.assertIsInstance(review["created_at"], str)
            self.assertIsInstance(review["updated_at"], str)

    def test_get_reviews_unauthenticated(self):
        """
        Test that unauthenticated users cannot access reviews list
        """
        url = reverse('review-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_reviews_authenticated(self):
        """
        Test that authenticated users can access reviews list
        """
        url = reverse('review-list')
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_review_as_customer(self):
        """
        Test that customers can create reviews
        """
        new_business_user = CustomUser.objects.create_user(
            username="anotherbusiness",
            password="testpass123",
            type='business'
        )
        BusinessProfile.objects.create(
            user=new_business_user,
            location="Another Location",
            tel="111111111",
            description="Another Description",
            working_hours="8 AM - 4 PM"
        )
        url = reverse('review-list')
        self.client.force_authenticate(user=self.customer_user)
        data = {
            'business_user': new_business_user.id,
            'rating': 5,
            'description': 'Great service!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_review_as_business(self):
        """
        Test that business users cannot create reviews
        """
        url = reverse('review-list')
        self.client.force_authenticate(user=self.business_user)
        data = {
            'business_user': self.business_profile.id,
            'reviewer': self.customer_profile.id,
            'rating': 5,
            'description': 'Great service!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_review_unauthenticated(self):
        """
        Test that unauthenticated users cannot create reviews
        """
        url = reverse('review-list')
        data = {
            'business_user': self.business_profile.id,
            'reviewer': self.customer_profile.id,
            'rating': 5,
            'description': 'Great service!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_review_as_creator(self):
        """
        Test that the creator can update their review
        """
        url = reverse('single-review', kwargs={'pk': self.review.pk})
        self.client.force_authenticate(user=self.customer_user)
        data = {'rating': 3, 'description': 'Updated review'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_review_as_non_creator(self):
        """
        Test that non-creators cannot update reviews
        """
        other_customer = CustomUser.objects.create_user(
            username="othercustomer",
            password="testpass123",
            type='customer'
        )
        url = reverse('single-review', kwargs={'pk': self.review.pk})
        self.client.force_authenticate(user=other_customer)
        data = {'rating': 3, 'description': 'Updated review'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_review_as_creator(self):
        """
        Test that the creator can delete their review
        """
        url = reverse('single-review', kwargs={'pk': self.review.pk})
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_review_as_non_creator(self):
        """
        Test that non-creators cannot delete reviews
        """
        other_customer = CustomUser.objects.create_user(
            username="othercustomer2",
            password="testpass123",
            type='customer'
        )
        url = reverse('single-review', kwargs={'pk': self.review.pk})
        self.client.force_authenticate(user=other_customer)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Further API tests covering invalid body data

    def test_post_review_invalid_rating(self):
        """
        Test that posting a review with an invalid rating returns a 400 status message
        """
        url = reverse('review-list')
        self.client.force_authenticate(user=self.customer_user)
        data = {
            'business_user': self.business_profile.id,
            'reviewer': self.customer_profile.id,
            'rating': 'invalid_rating', 
            'description': 'Great service' 
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_review_missing_fields(self):
        """
        Test that posting a review with missing required fields returns a 400 status
        """
        url = reverse('review-list')
        self.client.force_authenticate(user=self.customer_user)
        data = {
            'business_user': self.business_profile.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_review_invalid_rating(self):
        """
        Test that updating a review with an invalid rating returns a 400 status
        """
        url = reverse('single-review', kwargs={'pk': self.review.pk})
        self.client.force_authenticate(user=self.customer_user)
        data = {
            'rating': 'invalid_rating',
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_review_invalid_description(self):
        """
        Test that updating a review with an invalid descriptions returns a 400 status
        """
        url = reverse('single-review', kwargs={'pk': self.review.pk})
        self.client.force_authenticate(user=self.customer_user)
        data = {
            'description': 12345,
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_duplicate_review(self):
        """
        Test that a customer cannot submit multiple reviews for the same business_user
        """
        new_business_user = CustomUser.objects.create_user(
            username="newbusiness",
            password="testpass123",
            type='business'
        )
        BusinessProfile.objects.create(
            user=new_business_user,
            location="New Location",
            tel="987654321",
            description="New Description",
            working_hours="10 AM - 6 PM"
        )

        url = reverse('review-list')
        self.client.force_authenticate(user=self.customer_user)
        data = {
            'business_user': new_business_user.id,
            'rating': 5,
            'description': 'Great Service!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {
            'business_user': new_business_user.id,
            'rating': 4, 
            'description': 'Another review for the same business'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_review_with_string_numeric_rating(self):
        """Posting a review with rating as a numeric string should be rejected."""
        url = reverse('review-list')
        self.client.force_authenticate(user=self.customer_user)

        data = {
            'business_user': self.business_profile.id,
            'rating': "5",
            'description': 'Great Service'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_review_with_string_numeric_rating(self):
        """Patching a review with rating as a numeric string should be rejected."""
        url = reverse('single-review', kwargs={'pk': self.review.pk})
        self.client.force_authenticate(user=self.customer_user)
        data = {
            'rating': "4"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('rating', response.data)