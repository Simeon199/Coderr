from rest_framework import permissions
from profile_app.models import CustomerProfile
from reviews_app.models import Review
from rest_framework import serializers

class IsUserWarranted(permissions.BasePermission):
    """Allow only authenticated customers to POST reviews"""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        # Auth and role check
        if not self._is_customer(request.user):
            return False
        
        # Prevent duplicate review
        business_id = request.data.get("business_user")
        if business_id and self._has_reviewed(request.user, business_id):
            raise serializers.ValidationError(
                "You have already reviewed this business user."
            )
        return True
    
    def _is_customer(self, user) -> bool:
        return user.is_authenticated and getattr(user, "type", None) == "customer"
    
    def _has_reviewed(self, user, business_id: int) -> bool:
        try:
            profile = CustomerProfile.objects.get(user=user)
        except CustomerProfile.DoesNotExist:
            return False
        return Review.objects.filter(
            reviewer=profile,
            business_user=business_id
        ).exists()
    

class IsValidRating(permissions.BasePermission):
    """Reject non-int ratings or out-of-range values."""

    def has_permission(self, request, view) -> bool:
        if request.method in ("POST", "PATCH") and "rating" in request.data:
            self._validate_rating(request.data["rating"])
        return True
    
    def _validate_rating(self, rating):
        """Raise ValidationError on bad payload"""
        if isinstance(rating, int):
            value = rating
        elif isinstance(rating, str) and rating.isdigit():
            raise serializers.ValidationError(
                {"rating": "Rating must be an integer, not a string."}
            )
        else:
            raise serializers.ValidationError({"rating": "Invalid rating format."})
        
        if not 1 <= value <= 5:
            raise serializers.ValidationError(
                {"rating": "Rating must be between 1 and 5 inclusive."}
            )

class IsUserCreator(permissions.BasePermission):
    """Allow only the review's creator to modify/delete"""

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in ("PATCH", "DELETE"):
            return self._is_creator(request.user, obj)
        return True
    
    def _is_creator(self, user, obj):
        try:
            profile = CustomerProfile.objects.get(user=user)
        except CustomerProfile.DoesNotExist:
            return False
        return obj.reviewer == profile