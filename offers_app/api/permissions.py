from rest_framework.permissions import BasePermission


class IsOfferOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        return obj.user.id == request.user.id
