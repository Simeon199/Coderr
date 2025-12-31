from rest_framework import serializers
from offers_app.models import Offer, OfferDetail, UserDetails

class OfferDetailSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']
        read_only_fields = ['id', 'url']

    def get_url(self, obj):
        return f"/offerdetails/{obj.id}/"

class UserDetailsSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()

class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(source='offer_details', many=True, read_only=True)
    user_details = UserDetailsSerializer(source='user', read_only=True)

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']
        read_only_fields = ['id', 'created_at', 'updated_at', 'min_price', 'min_delivery_time', 'user_details', 'details']

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
            offer.min_price = min((detail.price for detail in offer.offer_details.all() if detail.price), default=None)
            offer.min_delivery_time = min((detail.delivery_time_in_days for detail in offer.offer_details.all() if detail.delivery_time_in_days), default=None)
            offer.save()
        return offer