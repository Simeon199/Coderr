from orders_app.models import Order, OrderFeatures
from rest_framework import generics
from .serializers import OrderListSerializers
from rest_framework.permissions import IsAuthenticated

class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializers
    permission_classes = [IsAuthenticated]