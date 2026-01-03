from orders_app.models import Order
from offers_app.models import OfferDetail
from rest_framework import generics
from rest_framework import status
from .serializers import OrderListSerializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializers
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        offer_detail_id = request.data.get('offer_detail_id')
        if not offer_detail_id:
            return Response({"error": "offer_detail_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            offer_detail = OfferDetail.objects.get(id=offer_detail_id)
        except OfferDetail.DoesNotExist:
            return Response({"error": "Invalid offer_detail_id"}, status=status.HTTP_404_NOT_FOUND)
        
        # Derive order data from the offer

        order_data = {
            'customer_user': offer_detail.user,
            'business_user': offer_detail.user,
            'title': offer_detail.title,
            'revisions': offer_detail.revisions,
            'delivery_time_in_days': offer_detail.delivery_time_in_days,
            'price': offer_detail.price,
            'features': offer_detail.features.all(),
            'offer_type': offer_detail.offer_type,
            'status': 'in_progress'
        }

        serializer = self.get_serializer(data=order_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)        