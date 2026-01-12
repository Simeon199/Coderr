from rest_framework import serializers
from reviews_app.models import Review

class SingleReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_description(self, value):
        if 'description' in self.initial_data and not isinstance(self.initial_data['description'], str):
            raise serializers.ValidationError("Description must be a string.")
        return value


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']