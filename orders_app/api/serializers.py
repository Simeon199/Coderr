from rest_framework import serializers
from orders_app.models import Order, OrderFeatures

class SingleOrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderFeatures
        fields = ['feature']

class OrderListSerializers(serializers.ModelSerializer):
    features = SingleOrderDetailSerializer(many=True)
    
    class Meta:
        model = Order
        fields = [
            "id", 
            "customer_user", 
            "business_user", 
            "title", 
            "revisions", 
            "delivery_time_in_days", 
            "price", 
            "features", 
            "offer_type", 
            "status", 
            "created_at", 
            "updated_at"
        ]
        read_only_fields = [
            "id", 
            "created_at", 
            "updated_at"
        ]

    def create(self, validated_data):
        features_data = validated_data.pop('features', [])
        offers = validated_data.pop('offers', None)
        offer_detail = validated_data.pop('offer_detail', None)
        order = Order.objects.create(**validated_data)
        if offers:
            order.offers = offers
            order.save()
        if offer_detail:
            order.offer_detail = offer_detail
            order.save()
        for feature_data in features_data:
            feature, created = OrderFeatures.objects.get_or_create(feature=feature_data['feature'])
            order.features.add(feature)
        return order
    
    def to_representation(self, instance):
        data = super().to_representation(instance) 
        data['features'] = [f.feature for f in instance.features.all()]
        return data