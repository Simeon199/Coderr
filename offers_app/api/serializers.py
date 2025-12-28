from rest_framework import serializers
from offers_app.models import Offer, OfferDetail, UserDetails

class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields =['first_name', 'last_name', 'username']

class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True, source='offer_details')
    user_details = UserDetailsSerializer(source='user.user_details', read_only=True)

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']
        read_only_fields = ['user_details', 'min_price', 'min_delivery_time', 'created_at', 'updated_at']

    def create(self, validated_data):
        offer_details_data = validated_data.pop('offer_details', [])
        offer = Offer.objects.create(**validated_data)
        for detail_data in offer_details_data:
            OfferDetail.objects.create(offer=offer, user=offer.user, **detail_data)
        return offer 
    
    def update(self, instance, validated_data):
        offer_details_data = validated_data.pop('offer_details', [])
        instance = super().update(instance, validated_data)
        instance.offer_details.all().delete()
        for detail_data in offer_details_data:
            OfferDetail.objects.create(offer=instance, **detail_data)
        return instance