from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from offers_app.models import Offer, OfferDetail
from orders_app.models import Order, OrderFeatures
from profile_app.models import BusinessProfile, CustomerProfile
from auth_app.models import CustomUser

class OrdersAPITestCase(APITestCase):
    def setUp(self):
        # Create test users
        self.user = CustomUser.objects.create_user(
            username = "john_doe",
            password="password24!",
            first_name="John",
            last_name="Doe",
            email="john.doe@testmail.com",
            type="business" # Default type; can be overwritten in child classes
        )

        # Generate a token for the user
        self.token = Token.objects.create(user=self.user)

        # Create a profile for the user
        if self.user.type == "business":
            self.profile = BusinessProfile.objects.create(
                user=self.user,
                username=self.user.username,
                first_name=self.user.first_name,
                last_name=self.user.last_name,
                file="",
                location="",
                tel="",
                description="",
                working_hours=""
            )
        else:
            self.profile = CustomerProfile.objects.create(
                user=self.user,
                username=self.user.username,
                first_name=self.user.first_name,
                last_name=self.user.last_name,
                file=""
            )

        self.customer_user = CustomUser.objects.create_user(
            username="bob_customer",
            password="password24!",
            first_name="Bob",
            last_name="Customer",
            email="bob.customer@testmail.com",
            type="customer"
        )

        self.business_user = CustomUser.objects.create_user(
            username="jane_doe",
            password="password24!",
            first_name="Jane",
            last_name="Doe",
            email="jane.business@testmail.com",
            type="business"
        )

        self.business_profile = BusinessProfile.objects.create(
            user = self.business_user,
            username = self.business_user.username,
            first_name = self.business_user.first_name,
            last_name = self.business_user.last_name,
            file="",
            location = "Los Angeles",
            tel = "1213456789",
            description = "Description",
            working_hours = "Everyday and every hour!"
        )

        self.customer_profile = CustomerProfile.objects.create(
            user = self.customer_user,
            username = self.customer_user.username,
            first_name = self.customer_user.first_name,
            last_name = self.customer_user.last_name,
            file=""
        )

        self.offer = Offer.objects.create(
            title = "Webseite Design",
            description = "Professionelles Webseite-Design",
            min_price = 100,
            min_delivery_time = 7,
            user=self.business_user # additional line as a foreign key
        )

        self.offerdetail = OfferDetail.objects.create(
            title = "Basic Design",
            revisions = 2,
            delivery_time_in_days = 5,
            price = 100,
            features = ["Logo Design", "Visitenkarte"],
            offer_type = "basic",
            offer = self.offer # additional line as a foreign key
        )

        # Following problem: We need to connect both customer_profile and business_profile to a customuser object!

        self.order = Order.objects.create(
            customer_user = self.customer_profile, 
            business_user = self.business_profile, 
            title = self.offerdetail.title,
            revisions = self.offerdetail.revisions,
            delivery_time_in_days = self.offerdetail.delivery_time_in_days,
            price = self.offerdetail.price,
            features = ['item_one', 'item_two'],
            offer_type = self.offerdetail.offer_type,
            status = 'in-progress',
            created_at = '2024-01-23T07:44:15.365773Z',
            updated_at = '2025-01-23T07:44:15.365773Z'
        )

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    # === GET ORDERS LIST TESTS ===

    def test_get_orders_structure(self):
        url = reverse('orders-list')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')

        # Check if the response status code is 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response data is a list
        self.assertIsInstance(response.data, list)

        # Chech if each order in the response has the required fields
        required_fields = {
            "id", "customer_user", "business_user", "title", "revisions", "delivery_time_in_days", "price", "features", "offer_type", "status", "created_at", "updated_at"
        }

        for order in response.data:
            self.assertTrue(required_fields.issubset(order.keys()))

            # Check the data types of the fields
            self.assertIsInstance(order["id"], int)
            self.assertIsInstance(order["customer_user"], int)
            self.assertIsInstance(order["business_user"], int)
            self.assertIsInstance(order["title"], str)
            self.assertIsInstance(order["revisions"], int)
            self.assertIsInstance(order["delivery_time_in_days"], int)
            self.assertIsInstance(order["price"], int)
            self.assertIsInstance(order["features"], list)
            self.assertIsInstance(order["offer_type"], str)
            self.assertIsInstance(order["status"], str)
            self.assertIsInstance(order["created_at"], str)
            self.assertIsInstance(order["updated_at"], str)

    def test_get_orders_unauthenticated(self):
        """Test that unauthenticated users cannot access the orders list"""
        url = reverse('orders-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_orders_authenticated(self):
        """Test that authenticated users can access the orders list"""
        url = reverse('orders-list')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # === POST ORDERS TESTS ===

    def test_post_order_as_authenticated_customer(self):
        """Checks whether an authenticated customer is able to create a new order"""
        url = reverse('orders-list')
        self.client.force_authenticate(user=self.customer_profile)
        data = {
            "offer_detail_id": self.offerdetail.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.data, dict)

        required_fields = {
            "id", "customer_user", "business_user", "title", "revisions", "delivery_time_in_days", "price", "features", "offer_type", "status", "created_at"
        }

        for order in response.data:
            self.assertTrue(required_fields.issubset(order.keys()))

            # Check the data types of the fields
            self.assertIsInstance(order["id"], int)
            self.assertIsInstance(order["customer_user"], int)
            self.assertIsInstance(order["business_user"], int)
            self.assertIsInstance(order["title"], str)
            self.assertIsInstance(order["revisions"], int)
            self.assertIsInstance(order["delivery_time_in_days"], int)
            self.assertIsInstance(order["price"], int)
            self.assertIsInstance(order["features"], list)
            self.assertIsInstance(order["offer_type"], str)
            self.assertIsInstance(order["status"], str)
            self.assertIsInstance(order["created_at"], str)

    def test_post_order_as_unauthenticated_user(self):
        url = reverse('orders-list')
        data = {
            "offer_detail_id": self.offerdetail.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_orders_as_authenticated_business_user(self):
        url = reverse('orders-list')
        self.client.force_authenticate(user=self.business_profile)
        data = {
            "offer_detail_id": self.offerdetail.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # === GET SINGLE ORDERS TEST ===

    def test_get_order_count_for_given_business_user(self):
        url = reverse('in-progress-order-count', kwargs={'pk': self.business_profile.user})
        self.client.force_authenticate(user=self.business_profile)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_order_count_fails_for_unauthenticated_user(self):
        url = reverse('in-progress-order-count', kwargs={'pk': self.business_profile.user})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_requested_business_user_for_order_count_doesnt_exit(self):
        """Test a 404 is returned when the requested business user does not exist"""
        url = reverse('in-progress-order-count', kwargs={'pk': 9999}) # Non-existent user ID
        self.client.force_authenticate(user=self.business_profile)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_completed_order_count_for_given_business_user(self):
        url = reverse('completed-order-count', kwargs={'pk': self.business_profile.user})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_completed_order_count_fails_for_unauthenticated_user(self):
        url = reverse('completed-order-count', kwargs={'pk': self.business_profile.user})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_requested_business_user_for_completed_order_count_doesnt_exit(self):
        """Test that a 404 is returned when the requested business user does not exist"""
        url = reverse('completed-order-count', kwargs={'pk': 9999})
        self.client.force_authenticate(user=self.business_profile)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # === PATCH SINGLE ORDERS ===

    def test_update_status_for_authenticated_business_user(self):
        """Test that an authenticated business user can update the status of an order"""
        url = reverse('single-order', kwargs={'pk': self.order.pk})
        self.client.force_authenticate(user=self.business_profile)
        data = {
            "status": "completed"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "completed")

    def test_update_status_failed_because_of_false_choices(self):
        """Test that updating the status with invalid choices fails"""
        url = reverse('single-order', kwargs={'pk': self.order.pk})
        self.client.force_authenticate(user=self.business_profile)
        data = {
            "status": "invalid_status"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_status_for_unauthenticated_user_fails(self):
        """Test that unauthenticated users cannot update the status of an order"""
        url = reverse('single-order', kwargs={'pk': self.order.pk})
        data = {
            "status": "completed"
        }        
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_status_for_authenticated_customer_user_is_not_permitted(self):
        """Test that authenticated customer users cannot uopdate the status of an order"""
        url = reverse('single-order', kwargs={'pk': self.order.pk})
        self.client.force_authenticate(user=self.customer_profile)
        data = {
            "status": "completed"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_status_failed_because_given_id_wasnt_found(self):
        """Test that updating the status of a non-existent order fails"""
        url = reverse('single-order', kwargs={'pk': 9999})
        self.client.force_authenticate(user=self.business_profile)
        data = {
            "status": "completed"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # === DELETE SINGLE ORDERS ===

    def test_order_deletion_successfull_for_admin_user(self):
        pass

    def test_order_deletion_failed_for_unauthenticated_user(self):
        pass

    def test_order_deletion_failed_because_user_is_no_admin(self):
        pass

    def test_order_deletion_failed_because_it_wasnt_found(self):
        pass