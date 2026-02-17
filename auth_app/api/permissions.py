from rest_framework.permissions import BasePermission, IsAuthenticated

from auth_app.models import UserProfile


class IsBusinessUser(BasePermission):
    """
    Permission class that allows access only to authenticated business users.

    This permission checks if the user is authenticated and has a UserProfile
    with type 'business'. Access is denied if the user is not authenticated,
    has no profile, or is not a business user.
    """

    def has_permission(self, request, view):
        """Return True if the user is authenticated and has a business profile."""
        if not IsAuthenticated().has_permission(request, view):
            return False

        user_profile = UserProfile.objects.filter(
            user_id=request.user.id
        ).first()
        if not user_profile:
            return False

        return user_profile.type == "business"


class IsCustomerUser(BasePermission):
    """
    Permission class that allows access only to authenticated customer users.

    This permission checks if the user is authenticated and has a UserProfile
    with type 'customer'. Access is denied if the user is not authenticated,
    has no profile, or is not a customer user.
    """

    def has_permission(self, request, view):
        """Return True if the user is authenticated and has a customer profile."""
        if not IsAuthenticated().has_permission(request, view):
            return False

        user_profile = UserProfile.objects.filter(
            user_id=request.user.id
        ).first()
        if not user_profile:
            return False

        return user_profile.type == "customer"


class IsAdminOrStaff(BasePermission):
    """
    Permission class that allows access only to staff or superuser accounts.

    This permission checks if the user has staff status or superuser privileges.
    Access is granted if either is_staff or is_superuser is True.
    """

    def has_permission(self, request, view):
        """Return True if the user has staff or superuser privileges."""
        user = request.user
        if not user:
            return False

        return user.is_staff or user.is_superuser


class IsProfileOwner(BasePermission):
    """Permission class that allows access only to the owner of a profile."""

    def has_object_permission(self, request, view, obj):
        """Return True if the requesting user is the owner of the object."""
        user = request.user

        return user.id == obj.id
