from rest_framework import serializers
from orders_app.models import Order, OrderFeatures


class SingleOrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderFeatures
        fields = ['feature']

class OrderListSerializers(serializers.ModelSerializer):
    features = SingleOrderDetailSerializer(source='orders', many=True)
    
    class Meta:
        model = Order
        fields = ["customer_user", "business_user", "title", "revisions", "delivery_time_in_days", "price", "features", "offer_type", "status", "created_at", "updated_at"]