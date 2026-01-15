from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from offers_app.models import Offer, OfferDetail, UserDetails
from profile_app.models import BusinessProfile, CustomerProfile
from auth_app.models import CustomUser

# I should also test whether the response is using the PageNumberPagination the right way

# Testing the query parameters is currently missing in my tests

class OffersAPITestCase(APITestCase):
    def setUp(self):
        # Create test users
        self.customer_user = CustomUser.objects.create_user(
            username="john_doe",
            password="password24!",
            type="customer"
        )

        self.business_user = CustomUser.objects.create_user(
            username="jane_doe",
            password="password24!",
            type="business"
        )

        # Create test instances of BusinessProfile and CustomerProfile
        self.business_profile = BusinessProfile.objects.create(
            user = self.business_user,
            username = self.business_user.username,
            first_name = "Jane",
            last_name = "Doe",
            location = "Los Angeles",
            tel = "1213456789",
            description = "Description",
            working_hours = "Everyday and every hour!"
        )

        self.customer_profile = CustomerProfile.objects.create(
            user = self.customer_user,
            username = self.customer_user.username,
            first_name = "John",
            last_name = "Doe"
        )

        # Offer object (new)

        self.offer = Offer.objects.create(
            title = "Webseite Design",
            description = "Professionelles Webseite-Design",
            min_price = 100,
            min_delivery_time = 7,
            user=self.business_user # additional line as a foreign key
        )

        self.offerdetail = OfferDetail.objects.create(
            # id = 1,
            title = "Basic Design",
            revisions = 2,
            delivery_time_in_days = 5,
            price = 100,
            features = ["Logo Design", "Visitenkarte"],
            offer_type = "basic",
            offer = self.offer # additional line as a foreign key
        )

    # === GET OFFERS LIST TESTS === 

    def test_get_offers_structure(self):
        """Test pagination structure is returned correctly"""
        url = reverse('offers-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check pagination fields
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)
        self.assertIsInstance(response.data['results'], list)

        # Check offer fields within results
        if response.data["results"]:
            offer = response.data['results'][0]
            required_fields = ["id", "user", "title", "description", "min_price", "min_delivery_time"]
            self.assertTrue(required_fields <= offer.keys())

    def test_pagination_structure(self):
        """Test pagination metadata is correct"""
        url = reverse('offers-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(response.data["count"], int)
        self.assertGreaterEqual(response.data["count"], 0)
        self.assertIsNone(response.data['previous']) # First page

    def test_filter_by_creator_id(self):
        """Test filtering offers by creator_id query parameter"""
        url = reverse('offers-list')
        response = self.client.get(f'{url}?creator_id={self.business_user.id}', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['count'], 2) # Two offers by business_user
        for offer in response.data["results"]:
            self.assertEqual(offer["user"], self.business_user.id)

    def test_filter_by_min_price(self):
        """Test filtering offers by min_price query parameter"""
        url = reverse('offers-list')
        response = self.client.get(f'{url}?min_price=200', format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for offer in response.data["results"]:
            self.assertGreaterEqual(offer["min_price"], 200)

    def test_filter_by_max_delivery_time(self):
        """Test filtering offers by max_delivery_time query parameter"""
        url=reverse('offers-list')
        response = self.client.get(f'{url}?max_delivery_time=7', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for offer in response.data['results']:
            self.assertLessEqual(offer['min_delivery_time'], 7)

    def test_search_by_title(self):
        """Test searching offers by title"""
        url = reverse('offers-list')
        response = self.client.get(f'{url}?search=Webseite', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(response.data['count'], 0)
        for offer in response.data['results']:
            self.assertIn('Webseite', offer['title'])

    def test_search_by_description(self):
        """Test searching offers by description"""
        url = reverse('offers-list')
        response = self.client.get(f'{url}?search=Professional', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(response.data['count'], 0)

    def test_ordering_by_min_price(self):
        """Test ordering offers by min_price"""
        url = reverse('offers-list')
        response = self.client.get(f'{url}?ordering=min_price', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        prices = [offer['min_price'] for offer in response.data["results"]]
        self.assertEqual(prices, sorted(prices))

    def test_combined_filters(self):
        """Test combining multiple filter parameters"""
        url = reverse('offers-list')
        response = self.client.get(
            f'{url}?creator_id={self.business_user.id}&min_price=100',
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for offer in response.data["results"]:
            self.assertEqual(offer["user"], self.business_user.id)
            self.assertGreaterEqual(offer["min_price"], 100)

    # === POST OFFERS TESTS ===

    def test_post_offers_as_customer_forbidden(self):
        """Test customer cannot create offers"""
        url = reverse('offers-list')
        self.client.force_authenticate(user=self.customer_user)
        data = {
            "title": "Grafikdesign-Paket",
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen",
            "details": []
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_offers_as_business_user(self):
        """Test business user can create offers"""
        url = reverse('offers-list')
        self.client.force_authenticate(user=self.business_user)
        data = {
            "title": "Grafikdesign-Paket",
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen",
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": ["Logo Design", "Visitenkarte"],
                    "offer_type": "basic"
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Grafikdesign-Paket")
        self.assertEqual(response.data["user"], self.business_user.id)

    def test_post_offers_unauthenticated(self):
        """Test unauthenticated user cannot create offers"""
        url = reverse('offers-list')
        data = {
            "title": "Test",
            "description": "Test",
            "details": []
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # === GET SINGLE OFFER TESTS ===

    # === PATCH OFFER TESTS ===

    # === DELETE OFFER TESTS ===

    # === OFFER DETAIL TESTS ===