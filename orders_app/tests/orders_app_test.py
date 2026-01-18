from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from offers_app.models import Offer, OfferDetail
from orders_app.models import Order, OrderFeatures
from profile_app.models import BusinessProfile, CustomerProfile
from auth_app.models import CustomUser

class OrdersAPITestCase(APITestCase):
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

        Order.objects.create(
            customer_user = self.customer_profile, # part of orders response
            business_user = self.business_profile, # part of orders response
            title = self.offerdetail.title,
            revisions = self.offerdetail.revisions,
            delivery_time_in_days = self.offerdetail.delivery_time_in_days,
            price = self.offerdetail.price,
            features = ['item_one', 'item_two'],
            offer_type = self.offerdetail.offer_type,
            status = 'in-progress',
            created_at = '',
            updated_at = ''
            # offer = self.offer,
            # offerdetail = self.offerdetail
        )

    # === GET ORDERS LIST TESTS ===

    def test_get_orders_structure(self):
        pass