from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from auth_app.api.permissions import IsCustomerUser
from reviews_app.api.permissions import IsReviewCreator
from reviews_app.api.serializers import (
    BaseReviewSerializer,
    CreateReviewSerializer,
)
from reviews_app.models import Review


class ReviewsViewSet(ModelViewSet):
    """
    ViewSet for managing reviews.

    Provides CRUD operations for reviews with role-based permissions.
    Customer users can create reviews, and only the review creator can
    update or delete their own reviews.
    """

    serializer_class = BaseReviewSerializer
    queryset = Review.objects.all()

    def get_permissions(self):
        """Return permissions based on the current action and user role."""
        if self.action == "create":
            return [IsAuthenticated(), IsCustomerUser()]
        if self.action == "partial_update":
            return [IsAuthenticated(), IsReviewCreator()]
        if self.action == "destroy":
            return [IsAuthenticated(), IsReviewCreator()]
        return super().get_permissions()

    def get_serializer_class(self):
        """Use create serializer for create actions."""
        if self.action == "create":
            return CreateReviewSerializer
        return super().get_serializer_class()
