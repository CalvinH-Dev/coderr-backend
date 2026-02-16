from rest_framework.permissions import BasePermission


class IsReviewCreator(BasePermission):
    """
    Permission class that allows access only to the creator of a review.

    This permission checks if the authenticated user is the reviewer who
    created the review object. Access is granted only if the user matches
    the review's reviewer.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.reviewer.id
