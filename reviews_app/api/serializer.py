from rest_framework import serializers
from reviews_app.models import Review
from profile_app.models import CustomerProfile

class SingleReviewSerializer(serializers.ModelSerializer):
    business_user = serializers.PrimaryKeyRelatedField(
        queryset=CustomerProfile.objects.all(),
        write_only=False
    )
    reviewer = serializers.StringRelatedField(read_only=True)
    # business_user = serializers.CharField(source="business_user.id", read_only=False)
    # reviewer = serializers.CharField(source="reviewer.id", read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_description(self, value):
        if 'description' in self.initial_data and not isinstance(self.initial_data['description'], str):
            raise serializers.ValidationError("Description must be a string.")
        return value


class ReviewListSerializer(serializers.ModelSerializer):
    business_user = serializers.CharField(source="business_user.id", read_only=False)
    reviewer = serializers.CharField(source="reviewer.id", read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']