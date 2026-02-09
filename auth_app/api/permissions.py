from rest_framework.permissions import BasePermission

from auth_app.models import UserProfile


class IsBusinessUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user:
            return False
        user_profile = UserProfile.objects.filter(user_id=user.id).first()
        if not user_profile:
            return False

        if user_profile.type == "business":
            return True

        return False
