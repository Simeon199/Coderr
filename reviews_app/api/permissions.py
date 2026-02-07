from rest_framework import permissions
from profile_app.models import CustomerProfile
from reviews_app.models import Review
from rest_framework import serializers
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class IsUserWarranted(permissions.BasePermission):
    """Allow only authenticated customers to POST reviews"""

    def has_permission(self, request, view):
        """Check if the requesting user is allowed to create or view reviews."""
        business_id = request.data.get("business_user")
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        if not self._is_customer(request.user):
            return False
        if business_id and self._has_reviewed(request.user, business_id):
            raise serializers.ValidationError("You have already reviewed this business user.")
        return True
    
    def _is_customer(self, user) -> bool:
        """Return True if the user is authenticated and has the customer type."""
        return user.is_authenticated and getattr(user, "type", None) == "customer"
    
    def _has_reviewed(self, user, business_id: int) -> bool:
        """Return True if the user has already submitted a review for the given business."""
        try:
            profile = CustomerProfile.objects.get(user=user)
        except CustomerProfile.DoesNotExist:
            return False
        return Review.objects.filter(reviewer=profile.user.id, business_user=business_id).exists()

class IsValidRating(permissions.BasePermission):
    """Reject non-int ratings or out-of-range values."""

    def has_permission(self, request, view) -> bool:
        """Validate the rating field on POST and PATCH requests."""
        if request.method in ("POST", "PATCH") and "rating" in request.data:
            self._validate_rating(request.data["rating"])
        return True
    
    def _validate_rating(self, rating):
        """Raise ValidationError on bad payload"""

        if isinstance(rating, int):
            value = rating
        elif isinstance(rating, str) and rating.isdigit():
            raise serializers.ValidationError({"rating": "Rating must be an integer, not a string."})
        else:
            raise serializers.ValidationError({"rating": "Invalid rating format."})
        if not 1 <= value <= 5:
            raise serializers.ValidationError({"rating": "Rating must be between 1 and 5 inclusive."})

class IsUserCreator(permissions.BasePermission):
    """Allow only the review's creator to modify/delete"""

    def has_object_permission(self, request, view, obj) -> bool:
        """Restrict PATCH and DELETE to the review's original creator."""
        if request.method in ("PATCH", "DELETE"):
            return self._is_creator(request.user, obj)
        return True
    
    def _is_creator(self, user, obj):
        """Return True if the user's customer profile matches the review's reviewer."""
        try:
            profile = CustomerProfile.objects.get(user=user)
        except CustomerProfile.DoesNotExist:
            return False
        return obj.reviewer == profile
