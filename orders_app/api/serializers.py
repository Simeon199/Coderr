from rest_framework import serializers
from orders_app.models import Order, OrderFeatures

class SingleOrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderFeatures
        fields = ['feature']

class OrderListSerializers(serializers.ModelSerializer):
    features = SingleOrderDetailSerializer(many=True)
    # offer_detail_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Order
        fields = ["id", "customer_user", "business_user", "title", "revisions", "delivery_time_in_days", "price", "features", "offer_type", "status", "created_at", "updated_at"]
        read_only_fields = ["id", "customer_user", "business_user", "title", "revisions", "delivery_time_in_days", "price", "features", "offer_type", "status", "created_at", "updated_at"]

    def create(self, validated_data):
        features_data = validated_data.pop('features')
        order = Order.objects.create(**validated_data)
        for feature_data in features_data:
            feature, created = OrderFeatures.objects.get_or_create(feature=feature_data['feature'])
            order.features.add(feature)
        return order
    
    def to_representation(self, instance):
        data = super().to_representation(instance) # default output
        data['features'] = [f.feature for f in instance.features.all()]
        return data