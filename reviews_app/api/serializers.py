from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from reviews_app.models import Review


class BaseReviewSerializer(serializers.ModelSerializer):
    """
    Base serializer for review objects.

    Provides common fields for review serialization including rating,
    description, and user relationships.
    """

    class Meta:
        model = Review
        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at",
        ]

        read_only_fields = ["created_at", "updated_at"]


class CreateReviewSerializer(BaseReviewSerializer):
    """
    Serializer for creating new reviews.

    Handles review creation by automatically setting the reviewer to the
    authenticated user and preventing duplicate reviews. A user can only
    submit one review per business user.

    Additional Fields:
        user (User): Hidden field auto-populated with current user.
    """

    user = serializers.HiddenField(
        default=CurrentUserDefault(), write_only=True
    )

    class Meta(BaseReviewSerializer.Meta):
        model = Review
        fields = BaseReviewSerializer.Meta.fields + ["user"]
        read_only_fields = BaseReviewSerializer.Meta.read_only_fields + [
            "reviewer"
        ]

    def create(self, validated_data):
        """
        Create a review after validating no duplicate exists for
        the business user.
        """
        validated_data.pop("user")
        reviewer = self.context["request"].user
        validated_data["reviewer"] = reviewer
        if Review.objects.filter(
            business_user=validated_data["business_user"], reviewer=reviewer
        ).exists():
            raise serializers.ValidationError(
                {"error": "You have already reviewed this business user."}
            )

        return super().create(validated_data)
