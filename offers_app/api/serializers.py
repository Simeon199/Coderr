from rest_framework import serializers
from offers_app.models import Offer, OfferDetail, UserDetails

class OfferDetailSerializer(serializers.ModelSerializer):
    # class Meta:
    #     model = OfferDetail
    #     fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']
    
    url = serializers.SerializerMethodField()
    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        return f'/offerdetails/{obj.id}/'

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
        # Calculate and set mins
        if offer.offer_details.exists():
            offer.min_price = min(detail.price for detail in offer.offer_details.all() if detail.price)
            offer.min_delivery_time = min(detail.delivery_time_in_days for detail in offer.offer_details.all() if detail.delivery_time_in_days)
        offer.sace()
        return offer

    def update(self, instance, validated_data):
        offer_details_data = validated_data.pop('offer_details', [])
        instance = super().update(instance, validated_data)
        instance.offer_details.all().delete()
        for detail_data in offer_details_data:
            OfferDetail.objects.create(offer=instance, **detail_data)
        if instance.offer_details.exists():
            instance.min_price = min(detail.price for detail in instance.offer_details.all() if detail.price)
            instance.min_delivery_time = min(detail.delivery_time_in_days for detail in instance.offer_details.all() if detail.delivery_time_in_days)
        instance.save()
        return instance
    # def create(self, validated_data):
    #     offer_details_data = validated_data.pop('offer_details', [])
    #     offer = Offer.objects.create(**validated_data)
    #     for detail_data in offer_details_data:
    #         OfferDetail.objects.create(offer=offer, user=offer.user, **detail_data)
    #     return offer 
    
    # def update(self, instance, validated_data):
    #     offer_details_data = validated_data.pop('offer_details', [])
    #     instance = super().update(instance, validated_data)
    #     instance.offer_details.all().delete()
    #     for detail_data in offer_details_data:
    #         OfferDetail.objects.create(offer=instance, **detail_data)
    #     return instance