from sqlite3 import IntegrityError

from django.forms import ValidationError
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from reviews_app.models import Review


class BaseReviewSerializer(serializers.ModelSerializer):
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
