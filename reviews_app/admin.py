from django.contrib import admin
from django.db.models import Avg

from reviews_app.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Admin interface for Review model.

    Provides comprehensive review management with rating statistics,
    filtering by business user and rating, and search capabilities.
    """

    list_display = [
        "id",
        "business_user",
        "reviewer",
        "rating",
        "get_short_description",
        "created_at",
    ]
    list_filter = [
        "rating",
        "business_user",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "business_user__username",
        "reviewer__username",
        "description",
    ]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        (
            "Review Information",
            {"fields": ("business_user", "reviewer", "rating")},
        ),
        ("Review Content", {"fields": ("description",)}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    list_per_page = 25
    ordering = ["-created_at"]

    actions = ["calculate_average_rating"]

    def get_short_description(self, obj):
        """
        Get a shortened version of the review description.

        Args:
            obj (Review): The review instance.

        Returns:
            str: First 50 characters of description with ellipsis if truncated.
        """
        if len(obj.description) > 50:
            return f"{obj.description[:50]}..."
        return obj.description

    get_short_description.short_description = "Description"

    def calculate_average_rating(self, request, queryset):
        """
        Admin action to calculate average rating for selected reviews.

        Args:
            request: The HTTP request object.
            queryset: QuerySet of selected Review objects.
        """
        avg_rating = queryset.aggregate(Avg("rating"))["rating__avg"]
        if avg_rating:
            self.message_user(
                request,
                f"Average rating for {queryset.count()} review(s): "
                f"{avg_rating:.2f} stars",
            )
        else:
            self.message_user(request, "No reviews selected.")

    calculate_average_rating.short_description = "Calculate average rating"
