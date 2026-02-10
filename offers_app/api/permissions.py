from rest_framework import permissions

class SingleOfferPermission(permissions.BasePermission):
    """
    Manage object-level access for individual offers.
    """

    def has_permission(self, request, view):
        """
        Ensure the user is authenticated before the object is loaded.
        """
        
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Allow safe methods for authenticated users and PATCH/DELETE only for the offer creator.
        """

        user = request.user
        is_creator = obj.user == user
        if request.method in permissions.SAFE_METHODS:
            return user and user.is_authenticated
        if request.method == 'PATCH':
            return is_creator
        if request.method == 'DELETE':
            return is_creator

class SingleOfferDetailPermission(permissions.BasePermission):
    """
    Manage object-level access for offer details.
    """

    def has_permission(self, request, view):
        """
        Ensure the user is authenticated before the object is loaded.
        """

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Allow safe methods only for authenticated users.
        """

        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

class IsBusinessUser(permissions.BasePermission):
    """
    Custom permission to only allow business users to create offers.
    """
    def has_permission(self, request, view):
        """
        Restrict POST requests to authenticated business users; allow all other methods.
        """
        
        if request.method == 'POST':
            return request.user.is_authenticated and request.user.type == 'business'
        return True