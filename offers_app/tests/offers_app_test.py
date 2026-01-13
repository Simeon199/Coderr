from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from offers_app.models import Offer
from profile_app.models import BusinessProfile, CustomerProfile
from auth_app.models import CustomUser

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

    def test_get_offers_structure(self):
        # No authentication required here
        pass

    def test_post_offers_as_customer(self):
        pass

    def test_get_single_offer_unauthenticated(self):
        pass

    def test_get_single_offer_authenticated(self):
        pass

    def test_patch_offer_as_non_creator(self):
        pass

    def test_patch_offer_as_creator(self):
        pass

    def test_delete_single_offer_as_non_creator(self):
        pass

    def test_delete_single_offer_as_creator(self):
        pass

    def get_single_offer_details_unauthenticated(self):
        pass

    def get_single_offer_details_authenticated(self):
        pass