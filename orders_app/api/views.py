from django.db import models
from orders_app.models import Order
from offers_app.models import OfferDetail
from profile_app.models import CustomerProfile, BusinessProfile
from rest_framework import generics
from rest_framework import status
from .serializers import OrderListSerializers, SingleOrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializers
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        offer_detail_id = request.data.get('offer_detail_id')
        if not offer_detail_id:
            return Response({"error": "offer_detail_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            offer_detail_all = OfferDetail.objects.all()
            print(f"offer_detail_all: {offer_detail_all}")
            offer_detail = OfferDetail.objects.get(id=offer_detail_id)
        except OfferDetail.DoesNotExist:
            return Response({"error": "Invalid offer_detail_id"}, status=status.HTTP_404_NOT_FOUND)
        
        # Fetch profiles
        try:
            customer_user = request.user
            customer_profile = CustomerProfile.objects.get(user=customer_user)
        except CustomerProfile.DoesNotExist: 
            return Response({"error": "Customer profile not found for user"}, status=status.HTTP_400_BAD_REQUEST)
        business_user = offer_detail.user  
        
        if not business_user:
            return Response({"error": "No user associated with this offer detail"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            business_profile = BusinessProfile.objects.get(user=business_user)
        except BusinessProfile.DoesNotExist:
            return Response({"error": "Business profile not found for offer user"}, status=status.HTTP_400_BAD_REQUEST)
        

        # Derive order data from the offer (updated to include profiles and links)
        features_data = [{'feature': feature} for feature in offer_detail.features or []]

        order_data = {
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

        serializer = self.get_serializer(data=order_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = SingleOrderSerializer
    permission_classes = [IsAuthenticated]       

class InProgressOrderCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        business_user_id = self.kwargs.get('pk')
        in_progress_orders = Order.objects.filter(business_user=business_user_id, status='in_progress')
        count = in_progress_orders.count()
        return Response({"count": count})

class CompletedOrderCountView(generics.GenericAPIView):
    pass