from rest_framework import serializers
from offers_app.models import Offer, OfferDetail

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

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']
        read_only_fields = ['id', 'created_at', 'updated_at', 'min_price', 'min_delivery_time', 'details']

class SingleOfferUpdateSerializer(serializers.ModelSerializer):
    details = OfferDetailCreateSerializer(source='offer_details', many=True, required=False)

    class Meta:
        model = Offer
        fields = ['title', 'image', 'description', 'details']
        extra_kwargs = {
            'title': {'required': False},
            'image': {'required': False},
            'description': {'required': False},
        }

    # def validate_details(self, value):
    #     if value is not None and len(value) < 3:
    #         raise serializers.ValidationError("At least three offer details are required.")
    #     return value
    
    def update(self, instance, validated_data):
        details_data = validated_data.pop('offer_details', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details_data is not None:
            # Get existing details
            existing_details = {detail.id: detail for detail in instance.offer_details.all()}
            updated_ids = set()

            for detail_data in details_data:
                detail_id = detail_data.get('id')
                if detail_id and detail_id in existing_details:
                    # Update existing 
                    detail = existing_details[detail_id]
                    for attr, value in detail_data.items():
                        if attr != 'id':
                            setattr(detail, attr, value)
                    detail.save()
                    updated_ids.add(detail_id)
                else:
                    # Create new
                    features = detail_data.pop('features', [])
                    OfferDetail.objects.create(offer=instance, **detail_data)
        
            # Delete details not in the update
            for detail_id, detail in existing_details.items():
                if detail_id not in updated_ids:
                    detail.delete()

            # Recalculate min_price and min_delivery_time
            if instance.offer_details.exists():
                instance.min_price = min((d.price for d in instance.offer_details.all() if d.price), default=None)
                instance.min_delivery_time = min((d.delivery_time_in_days for d in instance.offer_details.all() if d.delivery_time_in_days), default=None)
            else:
                instance.min_price = None
                instance.min_delivery_time = None
            instance.save()

        return instance

class SingleOfferDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = []