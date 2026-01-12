from rest_framework import permissions
from profile_app.models import CustomerProfile
from reviews_app.models import Review
from rest_framework import serializers

class IsUserWarranted(permissions.BasePermission):
    """
    Custom permission to only allow customers to create reviews.
    """
    def has_permission(self, request, view):
        user = request.user
        if request.method in permissions.SAFE_METHODS:
            return user and user.is_authenticated
        if request.method == 'POST':
            if not (user.is_authenticated and user.type == 'customer'):
                return False
            # Check if the customer has already reviewed the business_user
            business_user_id = request.data.get('business_user')
            if business_user_id:
                try:
                    customer_profile = CustomerProfile.objects.get(user=user)
                    existing_review = Review.objects.filter(
                        reviewer=customer_profile,
                        business_user=business_user_id
                    ).exists()
                    if existing_review:
                        raise serializers.ValidationError("You have already reviewed this business user.")
                except CustomerProfile.DoesNotExist:
                    return False
            return True
        return True
    
class IsUserCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try: 
            customer_profile = CustomerProfile.objects.get(user=request.user)
        except CustomerProfile.DoesNotExist:
            return False
                
        is_creator = obj.reviewer == customer_profile
        if request.method == 'PATCH' or request.method == 'DELETE':
            return is_creator
        return True