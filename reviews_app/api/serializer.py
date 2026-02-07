from rest_framework import serializers
from reviews_app.models import Review


class SingleReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for creating, retrieving and updating a single review.
    Returns business_user and reviewer as their user IDs instead of profile IDs.
    """

    business_user = serializers.SerializerMethodField()
    reviewer = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_business_user(self, obj):
        """
        Return the user ID of the associated business profile, or None.
        """
        return obj.business_user.user.id if obj.business_user else None

    def get_reviewer(self, obj):
        """
        Return the user ID of the associated reviewer profile, or None.
        """
        return obj.reviewer.user.id if obj.reviewer else None

    def validate_description(self, value):
        """
        Validate that the description field is a string.
        Raises:
            ValidationError: If description is not a string.
        """
        if 'description' in self.initial_data and not isinstance(self.initial_data['description'], str):
            raise serializers.ValidationError("Description must be a string.")
        return value


class ReviewListSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for listing reviews.
    Returns business_user and reviewer as their user IDs instead of profile IDs.
    """

    business_user = serializers.SerializerMethodField()
    reviewer = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']

    def get_business_user(self, obj):
        """
        Return the user ID of the associated business profile, or None.
        """
        return obj.business_user.user.id if obj.business_user else None

    def get_reviewer(self, obj):
        """
        Return the user ID of the associated reviewer profile, or None.
        """
        return obj.reviewer.user.id if obj.reviewer else None