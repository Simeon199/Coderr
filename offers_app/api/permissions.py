from rest_framework import permissions

class SingleOfferPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        is_creator = obj.user == user
        if request.method in permissions.SAFE_METHODS:
            return user and user.is_authenticated
        if request.method == 'PATCH':
            return is_creator
        if request.method == 'DELETE':
            return is_creator

class SingleOfferDetailPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

class IsBusinessUser(permissions.BasePermission):
    """
    Custom permission to only allow business users to create offers.
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated and request.user.type == 'business'
        return True