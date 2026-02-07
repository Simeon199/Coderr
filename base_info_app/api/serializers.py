from rest_framework import serializers
from base_info_app.models import BaseInfo

class BaseInfoSerializer(serializers.ModelSerializer):
    """Read-only serializer exposing platform-wide statistics from the BaseInfo model."""

    class Meta:
        model = BaseInfo
        fields = ['review_count', 'average_rating', 'business_profile_count', 'offer_count']
        read_only_fields = ['review_count', 'average_rating', 'business_profile_count', 'offer_count']