from rest_framework import permissions

class IsUserOfTypeCustomer(permissions.BasePermission):
    """
    Allow access only to authenticated users whose ``type`` attribute is
    set to ``"customer"``.
    """

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and self._is_customer(user)
    
    @staticmethod
    def _is_customer(user) -> bool:
        """Return True if the user is a customer."""
        return getattr(user, "type", None) == "customer"


class IsUserOfTypeBusiness(permissions.BasePermission):
    """
    Allow access only to authenticated users whose ``type`` attribute is
    set to ``"business"``.
    """

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and self._is_business(user)
    
    @staticmethod
    def _is_business(user) -> bool:
        """Return True if the user is a business."""
        return getattr(user, "type", None) == "business"


class IsUserMemberOfStaff(permissions.BasePermission):
    """
    Permission class that checks if the authenticated user is a staff member.
    Assumes the User model has a boolean ``is_staff`` attribute (default Django).
    """

    def has_permission(self, request, view):
        # Ensure the user is authenticated first
        user = request.user
        return user.is_authenticated and getattr(user, "is_staff", False)
