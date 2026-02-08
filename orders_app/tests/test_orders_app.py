from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from offers_app.models import Offer, OfferDetail
from orders_app.models import Order, OrderFeatures
from profile_app.models import BusinessProfile, CustomerProfile
from auth_app.models import CustomUser

class OrdersAPITestCase(APITestCase):
    """
    Test suite covering CRUD operations, permissions and validation for the orders API.
    """

    def setUp(self):
        """
        Create users, profiles, an offer with detail and a sample order for testing.
        """

        self.user = CustomUser.objects.create_user(
            username = "john_doe",
            password="password24!",
            first_name="John",
            last_name="Doe",
            email="john.doe@testmail.com",
            type="business" 
        )

        self.admin_user = CustomUser.objects.create_user(
            username="admin_user",
            password="admin_password",
            first_name="Admin",
            last_name="User",
            email="admin@testmail.com",
            type="admin",
            is_staff=True,
            is_superuser=True
        )
        self.token = Token.objects.create(user=self.user)
        if self.user.type == "business":
            self.profile = BusinessProfile.objects.create(
                user=self.user,
                location="",
                tel="",
                description="",
                working_hours=""
            )
        else:
            self.profile = CustomerProfile.objects.create(
                user=self.user
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
            location = "Los Angeles",
            tel = "1213456789",
            description = "Description",
            working_hours = "Everyday and every hour!"
        )

        self.customer_profile = CustomerProfile.objects.create(
            user = self.customer_user
        )

        self.offer = Offer.objects.create(
            title = "Webseite Design",
            description = "Professionelles Webseite-Design",
            min_price = 100,
            min_delivery_time = 7,
            user=self.business_user 
        )

        self.offerdetail = OfferDetail.objects.create(
            title = "Basic Design",
            revisions = 2,
            delivery_time_in_days = 5,
            price = 100,
            features = ["Logo Design", "Visitenkarte"],
            offer_type = "basic",
            offer = self.offer 
        )

        self.order = Order.objects.create(
            customer_user = self.customer_profile, 
            business_user = self.business_profile, 
            title = self.offerdetail.title,
            revisions = self.offerdetail.revisions,
            delivery_time_in_days = self.offerdetail.delivery_time_in_days,
            price = self.offerdetail.price,
            offer_type = self.offerdetail.offer_type,
            status = 'in-progress',
            created_at = '2024-01-23T07:44:15.365773Z',
            updated_at = '2025-01-23T07:44:15.365773Z'
        )

        feature1 = OrderFeatures.objects.create(feature="feature_one")
        feature2 = OrderFeatures.objects.create(feature="feature_two")
        self.order.features.set([feature1, feature2])
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_get_orders_structure(self):
        """
        Verify that each order in the list contains all required fields with correct types.
        """

        url = reverse('orders-list')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        required_fields = {"id", "customer_user", "business_user", "title", "revisions", "delivery_time_in_days", "price", "features", "offer_type", "status", "created_at", "updated_at"}

        for order in response.data:
            self.assertTrue(required_fields.issubset(order.keys()))
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
        """
        Test that unauthenticated users cannot access the orders list.
        """

        url = reverse('orders-list')
        unauthenticated_client = APIClient()
        response = unauthenticated_client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_orders_authenticated(self):
        """
        Test that authenticated users can access the orders list.
        """

        url = reverse('orders-list')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_order_as_authenticated_customer(self):
        """
        Checks whether an authenticated customer is able to create a new order.
        """

        url = reverse('orders-list')
        self.client.force_authenticate(user=self.customer_user)
        data = {
            "offer_detail_id": self.offerdetail.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.data, dict)
        required_fields = {"id", "customer_user", "business_user", "title", "revisions", "delivery_time_in_days", "price", "features", "offer_type", "status", "created_at"}

        self.assertTrue(required_fields.issubset(response.data.keys()))
        self.assertIsInstance(response.data["id"], int)
        self.assertIsInstance(response.data["customer_user"], int)
        self.assertIsInstance(response.data["business_user"], int)
        self.assertIsInstance(response.data["title"], str)
        self.assertIsInstance(response.data["revisions"], int)
        self.assertIsInstance(response.data["delivery_time_in_days"], int)
        self.assertIsInstance(response.data["price"], int)
        self.assertIsInstance(response.data["features"], list)
        self.assertIsInstance(response.data["offer_type"], str)
        self.assertIsInstance(response.data["status"], str)
        self.assertIsInstance(response.data["created_at"], str)

    def test_post_order_as_unauthenticated_user(self):
        """
        Verify that unauthenticated users cannot create an order (401).
        """

        url = reverse('orders-list')
        data = {
            "offer_detail_id": self.offerdetail.pk
        }
        unauthenticated_client = APIClient()
        response = unauthenticated_client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_orders_as_authenticated_business_user(self):
        """
        Verify that business users cannot create an order (403).
        """

        url = reverse('orders-list')
        self.client.force_authenticate(user=self.business_user)
        data = {
            "offer_detail_id": self.offerdetail.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_order_count_for_given_business_user(self):
        """
        Verify that an authenticated user can retrieve the in-progress order count.
        """

        url = reverse('in-progress-order-count', kwargs={'pk': self.business_profile.user.pk})
        self.client.force_authenticate(user=self.business_user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_order_count_fails_for_unauthenticated_user(self):
        """
        Verify that unauthenticated users cannot retrieve the in-progress order count (401).
        """

        url = reverse('in-progress-order-count', kwargs={'pk': self.business_profile.user.pk})
        unauthenticated_client = APIClient()
        response = unauthenticated_client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_requested_business_user_for_order_count_doesnt_exit(self):
        """
        Test a 404 is returned when the requested business user does not exist.
        """

        url = reverse('in-progress-order-count', kwargs={'pk': 9999}) 
        self.client.force_authenticate(user=self.business_user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_completed_order_count_for_given_business_user(self):
        """
        Verify that an authenticated user can retrieve the completed order count.
        """

        url = reverse('completed-order-count', kwargs={'pk': self.business_profile.user.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_completed_order_count_fails_for_unauthenticated_user(self):
        """
        Verify that unauthenticated users cannot retrieve the completed order count (401).
        """

        url = reverse('completed-order-count', kwargs={'pk': self.business_profile.user.pk})
        unauthenticated_user = APIClient()
        response = unauthenticated_user.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_requested_business_user_for_completed_order_count_doesnt_exit(self):
        """
        Test that a 404 is returned when the requested business user does not exist.
        """

        url = reverse('completed-order-count', kwargs={'pk': 9999})
        self.client.force_authenticate(user=self.business_user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_status_for_authenticated_business_user(self):
        """
        Test that an authenticated business user can update the status of an order.
        """

        url = reverse('single-order', kwargs={'pk': self.order.pk})
        self.client.force_authenticate(user=self.business_user)
        data = {
            "status": "completed"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "completed")

    def test_update_status_failed_because_of_false_choices(self):
        """
        Test that updating the status with invalid choices fails.
        """

        url = reverse('single-order', kwargs={'pk': self.order.pk})
        self.client.force_authenticate(user=self.business_user)
        data = {
            "status": "invalid_status"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_status_for_unauthenticated_user_fails(self):
        """
        Test that unauthenticated users cannot update the status of an order.
        """

        url = reverse('single-order', kwargs={'pk': self.order.pk})
        unauthenticated_client = APIClient()
        data = {
            "status": "completed"
        }        
        response = unauthenticated_client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_status_for_authenticated_customer_user_is_not_permitted(self):
        """
        Test that authenticated customer users cannot uopdate the status of an order.
        """

        url = reverse('single-order', kwargs={'pk': self.order.pk})
        self.client.force_authenticate(user=self.customer_user)
        data = {
            "status": "completed"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_status_failed_because_given_id_wasnt_found(self):
        """
        Test that updating the status of a non-existent order fails.
        """

        url = reverse('single-order', kwargs={'pk': 9999})
        self.client.force_authenticate(user=self.business_user)
        data = {
            "status": "completed"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_order_deletion_successfull_for_admin_user(self):
        """
        Test that an admin user can successfully delete an order.
        """

        self.client.force_authenticate(user=self.admin_user)
        url=reverse('single-order', kwargs={'pk': self.order.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(pk=self.order.pk).exists())
    
    def test_order_deletion_failed_for_unauthenticated_user(self):
        """
        Test that unauthenticated users cannot delete an order.
        """

        url = reverse('single-order', kwargs={'pk': self.order.pk})
        unauthenticated_client = APIClient()
        response = unauthenticated_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_deletion_failed_because_user_is_no_admin(self):
        """
        Test that non-admin users cannot delete an order.
        """

        self.client.force_authenticate(user=self.customer_user)
        url = reverse('single-order', kwargs={'pk': self.order.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_order_deletion_failed_because_it_wasnt_found(self):
        """
        Test that deleting a non-existent order fails.
        """

        self.client.force_authenticate(user=self.admin_user)
        url = reverse('single-order', kwargs={'pk': 9999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)