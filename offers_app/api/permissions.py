from rest_framework.permissions import BasePermission


class IsOfferOwner(BasePermission):
    """
    Permission class that allows access only to the owner of an object.

    This permission checks if the authenticated user is the owner of the
    object being accessed. Access is denied if the user is not authenticated
    or is not the object's owner.
    """

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        return obj.user.id == request.user.id
