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

        # UserDetails could in theory replace the imported customer_profile and business_profile
        # UserDetails.objects.create()

        self.offerdetail = OfferDetail.objects.create(
            id = 1,
            title = "Basic Design",
            revisions = 2,
            delivery_time_in_days = 5,
            price = 100,
            features = ["Logo Design", "Visitenkarte"],
            offer_type = "basic"
        )

        self.offer = Offer.objects.create(
            count = 1,
            next = "http://127.0.0.1:8000/api/offers/?page=2",
            previous = "null", # real null value should also be allowed
            results = [
                {
                    "id": 1,
                    "user": 1,
                    "title": "Webseite Design",
                    "image": "null", # real null value should also be allowed
                    "description": "Professionelles Webseite-Design...",
                    "created_at": "2024-09-25T10:00:00Z",
                    "updated_at": "2024-09-28T12:00:00Z"
                }
            ],
            details = [
                {
                    "id": 1,
                    "url": "/offerdetails/1/"
                },
                {
                    "id": 2,
                    "url": "/offerdetails/2/"
                },
                {
                    "id": 3,
                    "url": "/offerdetails/3/"
                }
            ],
            min_price=100,
            min_delivery_time=7,
            user_details = {
                "first_name": "John",
                "last_name": "Doe",
                "username": "john_doe"
            }
        )

    def test_get_offers_structure(self):
        # No authentication required 
        url = reverse('offers-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        required_fields = ["count", "next", "previous", "results", "min_price", "min_delivery_time", "user_details"]
        for offer in response.data:
            self.assertTrue(required_fields.issubset(offer.keys()))

            # Check the data types of the fields
            self.assertIsInstance(offer["count"], int)
            self.assertIsInstance(offer["next"], str)
            self.assertIsInstance(offer["previous"], str) # null should also be possible
            self.assertIsInstance(offer["results"], dict) # The nested key "details" should be assigned to an array
            self.assertIsInstance(offer["min_price"], int)
            self.assertIsInstance(offer["min_delivery_time"], int)
            self.assertIsInstance(offer["user_details"], dict)


    def test_post_offers_as_customer(self):
        url = reverse('offers-list')
        self.client.force_authenticate(user=self.customer_user)
        data = {
            "title": "Grafikdesign-Paket",
            "image": "null", # Should really be a null value
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
                {
                "title": "Basic Design",
                "revisions": 2,
                "delivery_time_in_days": 5,
                "price": 100,
                "features": [
                    "Logo Design",
                    "Visitenkarte"
                ],
                "offer_type": "basic"
                },
                {
                "title": "Standard Design",
                "revisions": 5,
                "delivery_time_in_days": 7,
                "price": 200,
                "features": [
                    "Logo Design",
                    "Visitenkarte",
                    "Briefpapier"
                ],
                "offer_type": "standard"
                },
                {
                "title": "Premium Design",
                "revisions": 10,
                "delivery_time_in_days": 10,
                "price": 500,
                "features": [
                    "Logo Design",
                    "Visitenkarte",
                    "Briefpapier",
                    "Flyer"
                ],
                "offer_type": "premium"
                }
            ]
        }
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_offers_as_business(self):
        url = reverse('offers-list')
        self.client.force_authenticate(user=self.business_user)
        data = {
            "title": "Grafikdesign-Paket",
            "image": "null", # Should really be a null value
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
                {
                "title": "Basic Design",
                "revisions": 2,
                "delivery_time_in_days": 5,
                "price": 100,
                "features": [
                    "Logo Design",
                    "Visitenkarte"
                ],
                "offer_type": "basic"
                },
                {
                "title": "Standard Design",
                "revisions": 5,
                "delivery_time_in_days": 7,
                "price": 200,
                "features": [
                    "Logo Design",
                    "Visitenkarte",
                    "Briefpapier"
                ],
                "offer_type": "standard"
                },
                {
                "title": "Premium Design",
                "revisions": 10,
                "delivery_time_in_days": 10,
                "price": 500,
                "features": [
                    "Logo Design",
                    "Visitenkarte",
                    "Briefpapier",
                    "Flyer"
                ],
                "offer_type": "premium"
                }
            ]
        }
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_single_offer_unauthenticated(self):
        url = reverse('single-offer')
        self.client.force_authenticate(user=self.customer_user) # this should also apply to a business_user
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_single_offer_authenticated(self):
        url = reverse('single-offer')
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.get(url, format='json')
        required_fields = {
            "id", "user", "title", "image", "description", "created_at", "updated_at", "details", "min_price", "min_delivery_time"
        }
        for single_offer in response.data:
            self.assertTrue(required_fields.issubset(single_offer.keys()))
            
            # Check the data types of the fields
            self.assertIsInstance(single_offer["id"], int)
            self.assertIsInstance(single_offer["user"], int)
            self.assertIsInstance(single_offer["image"], str) # Should also apply to a null value
            self.assertIsInstance(single_offer["description"], str) # Should also apply to an textfield
            self.assertIsInstance(single_offer["created_at"], int) # Should apply to a Datetime
            self.assertIsInstance(single_offer["updated_at"], int) # Should apply to a Datetime
            self.assertIsInstance(single_offer["details"], list) # This list/array contains dictionaries as elements
            self.assertIsInstance(single_offer["min_price"], int)
            self.assertIsInstance(single_offer["min_delivery_time"], int)

        self.assertEqual(response.status_code, status.HTTP_200_OK) # Not sure If I can include this line here 

    def test_patch_offer_as_non_creator(self):
        url = reverse('single-offer', kwargs={'pk': self.offer.pk})
        self.client.force_authenticate(user=self.business_user) # customer_user shouldn't be permitted to patch
        data = {
            "title": "Updated Grafikdesign-Paket",
            "details": [
                {
                "title": "Basic Design Updated",
                "revisions": 3,
                "delivery_time_in_days": 6,
                "price": 120,
                "features": [
                    "Logo Design",
                    "Flyer"
                ],
                "offer_type": "basic"
                }
            ]
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_offer_as_creator(self):
        url = reverse('single-offer', kwargs={'pk': self.offer.pk})
        self.client.force_authenticate(user=self.business_user) # customer_user shouldn't be permitted to patch
        data = {
            "title": "Updated Grafikdesign-Paket",
            "details": [
                {
                "title": "Basic Design Updated",
                "revisions": 3,
                "delivery_time_in_days": 6,
                "price": 120,
                "features": [
                    "Logo Design",
                    "Flyer"
                ],
                "offer_type": "basic"
                }
            ]
        }
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_single_offer_as_non_creator(self):
        url = reverse('offers-list', self.offer.pk)
        self.client.force_authenticate(user=self.business_user)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # A test which checks an unauthenticated user who is trying to delete an offer is missing

    def test_delete_single_offer_as_creator(self):
        url = reverse('offers-list', self.offer.pk)
        self.client.force_authenticate(user=self.business_user)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def get_single_offer_details_unauthenticated(self):
        url = reverse('single-offer-detail', kwargs={'pk': self.offerdetail.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def get_single_offer_details_authenticated(self):
        url = reverse('single-offer-detail', kwargs={'pk': self.offerdetail.pk})
        self.client.force_authenticate(user=self.business_user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)