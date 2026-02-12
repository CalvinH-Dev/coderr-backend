from rest_framework.permissions import BasePermission, IsAuthenticated

from auth_app.models import UserProfile


class IsBusinessUser(BasePermission):
    def has_permission(self, request, view):
        # Erst IsAuthenticated prüfen
        if not IsAuthenticated().has_permission(request, view):
            return False

        user_profile = UserProfile.objects.filter(
            user_id=request.user.id
        ).first()
        if not user_profile:
            return False

        return user_profile.type == "business"


class IsCustomerUser(BasePermission):
    def has_permission(self, request, view):
        # Erst IsAuthenticated prüfen
        if not IsAuthenticated().has_permission(request, view):
            return False

        user_profile = UserProfile.objects.filter(
            user_id=request.user.id
        ).first()
        if not user_profile:
            return False

        return user_profile.type == "customer"


class IsAdminOrStaff(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user:
            return False

        return user.is_staff or user.is_superuser
