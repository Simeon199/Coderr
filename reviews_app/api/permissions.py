from rest_framework import permissions

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
        user = request.user
        is_creator = obj.reviewer == user
        if request.method == 'PATCH' or request.method == 'DELETE':
            return is_creator