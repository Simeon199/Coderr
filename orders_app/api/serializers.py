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
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = BusinessProfile
        fields = ['user_id', 'first_name', 'last_name', 'username']

class CustomerProfileNestedSerializer(serializers.ModelSerializer):
    """Nested serializer for CustomerProfile"""
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = CustomerProfile
        fields = ['user_id', 'first_name', 'last_name', 'username']

class OrderListSerializers(serializers.ModelSerializer):
    business_user = serializers.PrimaryKeyRelatedField(queryset=BusinessProfile.objects.all())
    customer_user = serializers.PrimaryKeyRelatedField(queryset=CustomerProfile.objects.all())
    features = serializers.PrimaryKeyRelatedField(many=True, queryset=OrderFeatures.objects.all())

    class Meta:
        model = Order
        fields = [
            "id", 
            "customer_user", 
            "business_user", 
            # "customer_user_id", 
            # "business_user_id",
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
        features = validated_data.pop('features', [])
        order = Order.objects.create(**validated_data)
        order.features.set(features)
        return order
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['features'] = [f.feature for f in instance.features.all()]
        if instance.business_user:
            data['business_user'] = instance.business_user.user.id
        if instance.customer_user:
            data['customer_user'] = instance.customer_user.user.id
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