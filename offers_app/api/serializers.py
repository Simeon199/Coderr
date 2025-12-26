from rest_framework import serializers
from offers_app.models import Offer, OfferDetail, UserDetails

class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields =['first_name', 'last_name', 'username']

class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True, read_only=True)
    user_details = UserDetailsSerializer(source='user.user_details', read_only=True)

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']
        