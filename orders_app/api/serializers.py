from rest_framework import serializers
from orders_app.models import Order, OrderFeatures
from profile_app.models import BusinessProfile, CustomerProfile

class SingleOrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderFeatures
        fields = ['feature']

class BusinessProfileNestedSerializer(serializers.ModelSerializer):
    """Nested serializer for BusinessProfile"""
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = BusinessProfile
        # fields = ['user_id', 'first_name', 'last_name', 'username', 'location', 'tel']

class CustomerProfileNestedSerializer(serializers.ModelSerializer):
    """Nested serializer for CustomerProfile"""
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = CustomerProfile
        fields = ['user_id', 'first_name', 'last_name', 'username']

class OrderListSerializers(serializers.ModelSerializer):
    business_user = BusinessProfileNestedSerializer(read_only=True)
    customer_user = CustomerProfileNestedSerializer(read_only=True)
    features = serializers.SlugRelatedField(
        many=True,
        slug_field='feature',
        queryset=OrderFeatures.objects.all()
    )

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
    
class SingleOrderSerializer(serializers.ModelSerializer):
    business_user = BusinessProfileNestedSerializer(read_only=True)
    customer_user = CustomerProfileNestedSerializer(read_only=True)
    features = serializers.SlugRelatedField(
        many=True,
        slug_field='feature',
        queryset=OrderFeatures.objects.all()
    )

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
    
    def update(self, instance, validated_data):
        features_data = validated_data.pop("features", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if features_data is not None:
            instance.features.set(features_data)
        return instance


# PROPOSED CHANGE (commented):
# After moving common name fields into `CustomUser`, the nested
# profile serializers can source those fields directly from the
# related user. Example below shows a minimal nested serializer
# for orders that exposes `first_name` and `last_name` via the
# profile's `user` relation.
#
# class BusinessProfileNestedSerializer(serializers.ModelSerializer):
#     user_id = serializers.IntegerField(source='user.id', read_only=True)
#     first_name = serializers.CharField(source='user.first_name', read_only=True)
#     last_name = serializers.CharField(source='user.last_name', read_only=True)
#     username = serializers.CharField(source='user.username', read_only=True)
#
#     class Meta:
#         model = BusinessProfile
#         fields = ['user_id', 'first_name', 'last_name', 'username']
