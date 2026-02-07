from django.db import models
from orders_app.models import Order, OrderFeatures
from offers_app.models import OfferDetail
from profile_app.models import CustomerProfile, BusinessProfile
from rest_framework import generics
from rest_framework import status
from .serializers import OrderListSerializers, SingleOrderSerializer
from .permissions import IsUserOfTypeBusiness, IsAdminOrSuperuser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class OrderListView(generics.ListCreateAPIView):
    """
    API view for listing all orders and creating new orders from offer details.
    """

    queryset = Order.objects.all()
    serializer_class = OrderListSerializers
    permission_classes = [IsAuthenticated]

    def _get_offer_detail(self, offer_detail_id):
        """
        Validate and retrieve the OfferDetail by ID.
        Returns (offer_detail, None) or (None, error_response).
        """
        if not offer_detail_id:
            return None, Response({"error": "offer_detail_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            return OfferDetail.objects.get(id=offer_detail_id), None
        except OfferDetail.DoesNotExist:
            return None, Response({"error": "Invalid offer_detail_id"}, status=status.HTTP_404_NOT_FOUND)

    def _get_customer_profile(self, user):
        """
        Retrieve the CustomerProfile for the given user.
        Returns (customer_profile, None) or (None, error_response).
        """
        try:
            return CustomerProfile.objects.get(user=user), None
        except CustomerProfile.DoesNotExist:
            return None, Response({"error": "Customer profile not found for user"}, status=status.HTTP_403_FORBIDDEN)

    def _get_business_profile(self, offer_detail):
        """
        Retrieve the BusinessProfile linked to the offer detail.
        Returns (business_profile, None) or (None, error_response).
        """
        business_user = offer_detail.user
        if not business_user:
            return None, Response({"error": "No user associated with this offer detail"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            return BusinessProfile.objects.get(user=business_user), None
        except BusinessProfile.DoesNotExist:
            return None, Response({"error": "Business profile not found for offer user"}, status=status.HTTP_400_BAD_REQUEST)

    def _validate_request(self, request):
        """
        Validate the request by retrieving offer detail, customer and business profiles.
        Returns (offer_detail, customer_profile, business_profile, None) or (None, None, None, error_response).
        """
        offer_detail, error = self._get_offer_detail(request.data.get('offer_detail_id'))
        if error:
            return None, None, None, error
        customer_profile, error = self._get_customer_profile(request.user)
        if error:
            return None, None, None, error
        business_profile, error = self._get_business_profile(offer_detail)
        if error:
            return None, None, None, error
        return offer_detail, customer_profile, business_profile, None

    def _create_order_features(self, offer_detail):
        """
        Create or retrieve OrderFeatures from the offer detail's feature list.
        Returns a list of feature IDs.
        """
        features_data = []
        for feature_name in (offer_detail.features or []):
            feature_obj, created = OrderFeatures.objects.get_or_create(feature=feature_name)
            features_data.append(feature_obj.id)
        return features_data

    def _build_order_data(self, customer_profile, business_profile, offer_detail, features_data):
        """
        Build the order data dictionary from validated profiles and offer detail.
        """
        return {
            'customer_user': customer_profile.id,
            'business_user': business_profile.id,
            'title': offer_detail.title,
            'revisions': offer_detail.revisions,
            'delivery_time_in_days': offer_detail.delivery_time_in_days,
            'price': offer_detail.price,
            'features': features_data,
            'offer_type': offer_detail.offer_type,
            'status': 'in_progress'
        }

    def _build_response(self, serializer):
        """
        Build the 201 response, excluding the updated_at field.
        """
        headers = self.get_success_headers(serializer.data)
        response_data = dict(serializer.data)
        response_data.pop('updated_at', None)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    def create(self, request, *args, **kwargs):
        """
        Create a new order from an offer detail ID.
        Validates profiles and builds order data from the linked offer.
        """
        offer_detail, customer_profile, business_profile, error = self._validate_request(request)
        if error:
            return error
        features_data = self._create_order_features(offer_detail)
        order_data = self._build_order_data(customer_profile, business_profile, offer_detail, features_data)
        serializer = self.get_serializer(data=order_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return self._build_response(serializer)


class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating and deleting a single order.
    GET requires authentication, PATCH requires business user type,
    DELETE requires admin or superuser permissions.
    """

    queryset = Order.objects.all()
    serializer_class = SingleOrderSerializer

    def get_permissions(self):
        """
        Return permission classes based on the HTTP method.
        """
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'PATCH':
            return [IsUserOfTypeBusiness()]
        elif self.request.method == 'DELETE':
            return [IsAdminOrSuperuser()]
        else:
            return super().get_permissions()


class InProgressOrderCountView(APIView):
    """
    API view that returns the count of in-progress orders for a business user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Return the number of orders with status 'in_progress' for the given business user.
        """
        business_user_id = self.kwargs.get('pk')
        if not BusinessProfile.objects.filter(user__id=business_user_id).exists():
            return Response(
                {"detail": "Business profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        order_count = Order.objects.filter(business_user=business_user_id, status='in_progress').count()
        return Response({"order_count": order_count})


class CompletedOrderCountView(APIView):
    """
    API view that returns the count of completed orders for a business user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Return the number of orders with status 'completed' for the given business user.
        """
        business_user_id = self.kwargs.get('pk')
        if not BusinessProfile.objects.filter(user__id=business_user_id).exists():
            return Response(
                {"detail": "Business profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        completed_order_count = Order.objects.filter(business_user=business_user_id, status='completed').count()
        return Response({"completed_order_count": completed_order_count})