from rest_framework import serializers
from reviews_app.models import Review

class SingleReviewSerializer(serializers.ModelSerializer):
    business_user = serializers.SerializerMethodField()
    reviewer = serializers.SerializerMethodField()
    # business_user = serializers.CharField(source="business_user.user.id", read_only=True)
    # reviewer = serializers.CharField(source="reviewer.user.id", read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_business_user(self, obj):
        return obj.business_user.user.id if obj.business_user else None

    def get_reviewer(self, obj):
        return obj.reviewer.user.id if obj.reviewer else None

    def validate_description(self, value):
        if 'description' in self.initial_data and not isinstance(self.initial_data['description'], str):
            raise serializers.ValidationError("Description must be a string.")
        return value


class ReviewListSerializer(serializers.ModelSerializer):
    # business_user = serializers.IntegerField(source="business_user.user.id", read_only=False)
    # reviewer = serializers.IntegerField(source="reviewer.user.id", read_only=True)
    business_user = serializers.SerializerMethodField()
    reviewer = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']

    def get_business_user(self, obj):
        return obj.business_user.user.id if obj.business_user else None
    
    def get_reviewer(self, obj):
        return obj.reviewer.user.id if obj.reviewer else None