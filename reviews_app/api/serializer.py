from rest_framework import serializers
from reviews_app.models import Review
from profile_app.models import CustomerProfile
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class SingleReviewSerializer(serializers.ModelSerializer):
    # business_user = serializers.PrimaryKeyRelatedField(
    #     queryset=CustomerProfile.objects.all(),
    #     write_only=False
    # )
    # business_user = serializers.SlugRelatedField(
    #     queryset=CustomUser.objects.all(),
    #     slug_field='username',
    # )
    # reviewer = serializers.StringRelatedField(read_only=True)
    business_user = serializers.CharField(source="business_user.id", read_only=False)
    reviewer = serializers.CharField(source="reviewer.id", read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_description(self, value):
        if 'description' in self.initial_data and not isinstance(self.initial_data['description'], str):
            raise serializers.ValidationError("Description must be a string.")
        return value


class ReviewListSerializer(serializers.ModelSerializer):
    # business_user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    # reviewer = serializers.SlugRelatedField(read_only=True, slug_field='user__username')
    business_user = serializers.CharField(source="business_user.id", read_only=False)
    reviewer = serializers.CharField(source="reviewer.id", read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']