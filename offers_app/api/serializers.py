from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from profile_app.models import CustomerProfile, BusinessProfile

class ProfileUpdateSerializer(serializers.Serializer):
    """
    Serializer for updating user profile fields (first_name, last_name)
    within an offer update request.
    """

    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

class OfferDetailListSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for listing offer details with their URL.
    """

    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']
        read_only_fields = ['id', 'url']

    def get_url(self, obj):
        """Return the detail URL for the given offer detail."""
        return f"/offerdetails/{obj.id}/"


class OfferDetailCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating offer detail entries.
    Features are accepted as a list of strings.
    """

    features = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )

    class Meta:
        model = OfferDetail
        fields = [
            'id', 
            'title', 
            'revisions', 
            'delivery_time_in_days', 
            'price', 
            'features', 
            'offer_type'
        ]
        read_only_fields = ['id']

class OfferCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating offers with nested offer details.
    Requires at least three detail entries.
    """

    details = OfferDetailCreateSerializer(source='offer_details', many=True)

    class Meta:
        model = Offer
        fields = [
            'id', 
            'title', 
            'image', 
            'description', 
            'details'
        ]
        read_only_fields = ['id']

    def validate_details(self, value):
        """
        Validate that the 'details' list contains at least three items.
        """
        if len(value) < 3:
            raise serializers.ValidationError("At least three offer details are required.")
        return value

    def create(self, validated_data):
        """
        Create an offer with nested details and calculate price/delivery aggregates.
        """
        details_data = validated_data.pop('offer_details', [])
        offer = Offer.objects.create(**validated_data)
        
        for detail_data in details_data:
            features = detail_data.pop('features', [])
            offer_detail = OfferDetail.objects.create(offer=offer, **detail_data)
            offer_detail.features = features
            offer_detail.save()
        
        if offer.offer_details.exists():
            offer.min_price = min((detail.price for detail in offer.offer_details.all() if detail.price), default=None)
            offer.min_delivery_time = min((detail.delivery_time_in_days for detail in offer.offer_details.all() if detail.delivery_time_in_days), default=None)
            offer.save()
        
        return offer

class UserDetailsSerializer(serializers.Serializer):
    """
    Read-only serializer for embedding basic user information in offer responses.
    """

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()

class OfferListSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for listing offers with nested details and user information.
    """

    details = OfferDetailListSerializer(source='offer_details', many=True, read_only=True)
    user_details = UserDetailsSerializer(source='user', read_only=True)

    class Meta:
        model = Offer
        fields = [
            'id', 
            'user', 
            'title', 
            'image', 
            'description', 
            'created_at', 
            'updated_at', 
            'details', 
            'min_price', 
            'min_delivery_time', 
            'user_details'
        ]
        read_only_fields = [
            'id', 
            'created_at', 
            'updated_at', 
            'min_price', 
            'min_delivery_time', 
            'user_details', 
            'details'
        ]


class SingleOfferSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for retrieving a single offer with nested details and user information.
    """

    details = OfferDetailListSerializer(source='offer_details', many=True, read_only=True)
    user_details = UserDetailsSerializer(source='user', read_only=True)

    class Meta:
        model = Offer
        fields = [
            'id', 
            'user',
            'title', 
            'image', 
            'description', 
            'created_at', 
            'updated_at', 
            'details', 
            'min_price', 
            'min_delivery_time', 
            'user_details'
        ] 
        read_only_fields = [
            'id', 
            'created_at', 
            'updated_at', 
            'min_price', 
            'min_delivery_time', 
            'details', 
            'user_details'
        ]

    def get_user_details(self, obj):
        """
        Return first_name, last_name and username for the offer's user,
        or None if no user is associated.
        """
        if obj.user:
            if obj.user.type == 'business':
                profile = obj.user.business_profile
            elif obj.user.type == 'customer':
                profile = obj.user.customer_profile
            else:
                return None
            return {
                'first_name': profile.first_name,
                'last_name': profile.last_name,
                'username': obj.user.username
            }
        return None

class SingleOfferUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating an offer with nested offer details.
    Supports partial updates of top-level fields and nested details.
    """

    details = OfferDetailCreateSerializer(source='offer_details', many=True, required=False)
    user_details = ProfileUpdateSerializer(required=False)

    class Meta:
        model = Offer
        fields = [
            'id', 
            'title', 
            'image', 
            'description', 
            'details', 
            'user_details'
        ]
        read_only_fields = ['id']
        extra_kwargs = {
            'title': {'required': False},
            'image': {'required': False},
            'description': {'required': False},
        }

    def to_representation(self, instance):
        """
        Use SingleOfferSerializer for output, excluding user, min_price and min_delivery_time.
        """
        representation = SingleOfferSerializer(instance).data
        representation.pop('user', None)
        representation.pop('min_price', None)
        representation.pop('min_delivery_time', None)
        return representation

    def _update_offer_fields(self, instance, validated_data):
        """
        Update top-level offer fields, excluding nested offer_details.
        """
        for attr, value in validated_data.items():
            if attr != 'offer_details':
                setattr(instance, attr, value)
        instance.save()

    def _update_or_create_details(self, instance, details_data):
        """
        Update existing or create new offer details for the given offer.
        """
        for detail_data in details_data:
            detail_id = detail_data.get('id')
            if detail_id:
                detail = instance.offer_details.get(id=detail_id)
                for attr, value in detail_data.items():
                    if attr != 'id':
                        setattr(detail, attr, value)
                detail.save()
            else:
                OfferDetail.objects.create(offer=instance, **detail_data)

    def _recalculate_aggregates(self, instance):
        """
        Recalculate min_price and min_delivery_time from all offer details.
        """
        details = instance.offer_details.all()
        instance.min_price = min((d.price for d in details if d.price), default=None)
        instance.min_delivery_time = min((d.delivery_time_in_days for d in details if d.delivery_time_in_days), default=None)
        instance.save()

    def update(self, instance, validated_data):
        """
        Update offer fields and nested offer details, then recalculate aggregates.
        """
        self._update_offer_fields(instance, validated_data)
        details_data = validated_data.get('offer_details')
        if details_data:
            self._update_or_create_details(instance, details_data)
            self._recalculate_aggregates(instance)
        return instance

class SingleOfferDeleteSerializer(serializers.ModelSerializer):
    """
    Empty serializer used for deleting an offer.
    """

    class Meta:
        model = Offer
        fields = []

class SingleOfferDetailSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for retrieving a single offer detail entry.
    """

    class Meta:
        model = OfferDetail
        fields = [
            'id', 
            'title', 
            'revisions', 
            'delivery_time_in_days', 
            'price', 
            'features', 
            'offer_type'
        ]