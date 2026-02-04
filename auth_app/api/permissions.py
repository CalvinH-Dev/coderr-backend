from rest_framework.permissions import IsAuthenticated

from core.exceptions import NotAuthorized


class IsAuthenticatedOr401(IsAuthenticated):
    """Permission class that returns 401 for unauthenticated users instead of 403."""

    def has_permission(self, request, view):
        """Return True if user is authenticated, raise NotAuthorized (401) otherwise."""
        if not request.user or not request.user.is_authenticated:
            raise NotAuthorized
        return True
