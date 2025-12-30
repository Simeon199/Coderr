from rest_framework import serializers
from offers_app.models import Offer, OfferDetail, UserDetails

class UserDetailsSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()

class OfferDetailSerializer(serializers.Serializer):
    model = OfferDetail
    fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']
    read_only_fields = ['id']

class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True, read_only=True)
    user_details = UserDetailsSerializer(source='user', read_only=True)

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']
        read_only_fields = ['id', 'created_at', 'updated_at', 'min_price', 'min_delivery_time', 'user_details']

    def validate_details(self, value):
        """
        Validate that the 'details' list contains at least three items.
        """
        if(len(value)<3):
            raise serializers.ValidationError("At least three offer details are required.")
        return value

    def create(self, validated_data):
        details_data = validated_data.pop('details', [])
        offer = Offer.objects.create(**validated_data)
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, user=offer.user, **detail_data)
        if offer.offer_details.exists():
            offer.min_price = min(detail.price for detail in offer.offer_details.all() if detail.price)
            offer.min_delivery_time = min(detail.delivery_time_in_days for detail in offer.offer_details.all() if detail.delivery_time_in_days)
            offer.save()
        return offer