from rest_framework import permissions
from profile_app.models import CustomerProfile

class IsUserWarranted(permissions.BasePermission):
    """
    Custom permission to only allow customers to create reviews.
    """
    def has_permission(self, request, view):
        user = request.user
        if request.method in permissions.SAFE_METHODS:
            return user and user.is_authenticated
        if request.method == 'POST':
            return user.is_authenticated and user.type == 'customer'
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