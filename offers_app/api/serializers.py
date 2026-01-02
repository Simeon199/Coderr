from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from profile_app.models import CustomerProfile, BusinessProfile

class ProfileUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

class OfferDetailListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']
        read_only_fields = ['id', 'url']

    def get_url(self, obj):
        return f"/offerdetails/{obj.id}/"


class OfferDetailCreateSerializer(serializers.ModelSerializer):
    features = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )

    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']
        read_only_fields = ['id']


class OfferCreateSerializer(serializers.ModelSerializer):
    details = OfferDetailCreateSerializer(source='offer_details', many=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']
        read_only_fields = ['id']

    def validate_details(self, value):
        """
        Validate that the 'details' list contains at least three items.
        """
        if len(value) < 3:
            raise serializers.ValidationError("At least three offer details are required.")
        return value

    def create(self, validated_data):
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
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()

class OfferListSerializer(serializers.ModelSerializer):
    details = OfferDetailListSerializer(source='offer_details', many=True, read_only=True)
    user_details = UserDetailsSerializer(source='user', read_only=True)

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']
        read_only_fields = ['id', 'created_at', 'updated_at', 'min_price', 'min_delivery_time', 'user_details', 'details']


class SingleOfferSerializer(serializers.ModelSerializer):
    details = OfferDetailListSerializer(source='offer_details', many=True, read_only=True)
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details'] 
        read_only_fields = ['id', 'created_at', 'updated_at', 'min_price', 'min_delivery_time', 'details', 'user_details']

    def get_user_details(self, obj):
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
    details = OfferDetailCreateSerializer(source='offer_details', many=True, required=False)
    user_details = ProfileUpdateSerializer(required=False)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details', 'user_details']
        read_only_fields = ['id']
        extra_kwargs = {
            'title': {'required': False},
            'image': {'required': False},
            'description': {'required': False},
        }

    def to_representation(self, instance):
        representation = SingleOfferSerializer(instance).data
        representation.pop('user', None)
        representation.pop('min_price', None)
        representation.pop('min_delivery_time', None)
        return representation
    
    def update(self, instance, validated_data):
        # Update basic offer fields
        for attr, value in validated_data.items():
            if attr not in ['offer_details', 'user_details']:
                setattr(instance, attr, value)
        instance.save()

        # Handle offer details
        details_data = validated_data.get('offer_details')
        if details_data:
            for detail_data in details_data:
                detail_id = detail_data.get('id')
                if detail_id:
                    # Update existing detail
                    detail = instance.offer_details.get(id=detail_id)
                    for attr, value in detail_data.items():
                        if attr != 'id':
                            setattr(detail, attr, value)
                    detail.save()
                else:
                    # Create new detail
                    OfferDetail.objects.create(offer=instance, **detail_data)
            
            # Recalculate min_price and min_delivery_time
            instance.min_price = min((d.price for d in instance.offer_details.all() if d.price), default=None)
            instance.min_delivery_time = min((d.delivery_time_in_days for d in instance.offer_details.all() if d.delivery_time_in_days), default=None)
            instance.save()

        # Handle user_details update
        user_details_data = validated_data.get('user_details')
        if user_details_data:
            if instance.user.type == 'business':
                profile = instance.user.business_profile
            elif instance.user.type == 'customer':
                profile = instance.user.customer_profile
            else:
                profile = None
            if profile:
                for attr, value in user_details_data.items():
                    setattr(profile, attr, value)
                profile.save()

        return instance

class SingleOfferDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = []

class SingleOfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']