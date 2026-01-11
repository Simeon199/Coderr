from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class ReviewAPITestCase(APITestCase):
    def test_get_reviews_structure(self):
        url = reverse('reviews-list')
        response = self.client.get(url, format='json')

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response data is a list
        self.assertIsInstance(response.data, list)

        # Check if each review in the response has the required fields
        required_fields = {
            "id", "business_user", "reviewer", "rating", "description", "created_at", "updated_at"
        }

        for review in response.data:
            self.assertTrue(required_fields.issubset(review.keys()))

            # Check the data types of the fields
            self.assertIsInstance(review["id"], int)
            self.assertIsInstance(review["business_user"], int)
            self.assertIsInstance(review["reviewer"], int)
            self.assertIsInstance(review["rating"], int)
            self.assertIsInstance(review["description"], str)
            self.assertIsInstance(review["created_at"], str)
            self.assertIsInstance(review["updated_at"], str)