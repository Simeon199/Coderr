from rest_framework import serializers
from orders_app.models import Order, OrderFeatures
from profile_app.models import BusinessProfile, CustomerProfile


class SingleOrderDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for a single order feature entry.
    """

    class Meta:
        model = OrderFeatures
        fields = ['feature']


class BusinessProfileNestedSerializer(serializers.ModelSerializer):
    """
    Nested read-only serializer for embedding business profile data in order responses.
    """

    user_id = serializers.IntegerField(source='user.id', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = BusinessProfile
        fields = ['user_id', 'first_name', 'last_name', 'username']


class CustomerProfileNestedSerializer(serializers.ModelSerializer):
    """
    Nested read-only serializer for embedding customer profile data in order responses.
    """

    user_id = serializers.IntegerField(source='user.id', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = CustomerProfile
        fields = ['user_id', 'first_name', 'last_name', 'username']


class OrderListSerializers(serializers.ModelSerializer):
    """
    Serializer for listing and creating orders.
    Accepts profile primary keys on input and returns user IDs on output.
    """

    business_user = serializers.PrimaryKeyRelatedField(queryset=BusinessProfile.objects.all())
    customer_user = serializers.PrimaryKeyRelatedField(queryset=CustomerProfile.objects.all())
    features = serializers.PrimaryKeyRelatedField(many=True, queryset=OrderFeatures.objects.all())

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
        """Create an order and assign the associated features."""
        features = validated_data.pop('features', [])
        order = Order.objects.create(**validated_data)
        order.features.set(features)
        return order

    def to_representation(self, instance):
        """
        Return user IDs instead of profile IDs for business_user and customer_user,
        and feature names instead of feature IDs.
        """
        data = super().to_representation(instance)
        data['features'] = [f.feature for f in instance.features.all()]
        if instance.business_user:
            data['business_user'] = instance.business_user.user.id
        if instance.customer_user:
            data['customer_user'] = instance.customer_user.user.id
        return data


class SingleOrderSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving, updating and deleting a single order.
    Features are referenced by their slug (feature name).
    """

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
        """
        Update order fields and reassign features if provided.
        """
        features_data = validated_data.pop("features", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if features_data is not None:
            instance.features.set(features_data)
        return instance

    def to_representation(self, instance):
        """
        Return user IDs instead of profile IDs for business_user and customer_user.
        """
        data = super().to_representation(instance)
        if instance.business_user:
            data['business_user'] = instance.business_user.user.id
        if instance.customer_user:
            data['customer_user'] = instance.customer_user.user.id
        return data
