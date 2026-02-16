from django.contrib import admin

from orders_app.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin interface for Order model.

    Provides comprehensive order management with status tracking,
    user filtering, and detailed order information display.
    """

    list_display = [
        "id",
        "title",
        "status",
        "customer_user",
        "business_user",
        "price",
        "delivery_time_in_days",
        "created_at",
    ]
    list_filter = [
        "status",
        "offer_type",
        "created_at",
        "updated_at",
        "business_user",
    ]
    search_fields = [
        "title",
        "customer_user__username",
        "business_user__username",
    ]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        ("Order Information", {"fields": ("title", "status", "offer_type")}),
        ("Users", {"fields": ("customer_user", "business_user")}),
        (
            "Order Details",
            {
                "fields": (
                    "price",
                    "delivery_time_in_days",
                    "revisions",
                    "features",
                )
            },
        ),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    list_per_page = 25
    ordering = ["-created_at"]

    actions = ["mark_as_completed", "mark_as_cancelled", "mark_as_in_progress"]

    def mark_as_completed(self, request, queryset):
        """
        Admin action to mark selected orders as completed.

        Args:
            request: The HTTP request object.
            queryset: QuerySet of selected Order objects.
        """
        updated = queryset.update(status="completed")
        self.message_user(request, f"{updated} order(s) marked as completed.")

    mark_as_completed.short_description = "Mark selected orders as completed"

    def mark_as_cancelled(self, request, queryset):
        """
        Admin action to mark selected orders as cancelled.

        Args:
            request: The HTTP request object.
            queryset: QuerySet of selected Order objects.
        """
        updated = queryset.update(status="cancelled")
        self.message_user(request, f"{updated} order(s) marked as cancelled.")

    mark_as_cancelled.short_description = "Mark selected orders as cancelled"

    def mark_as_in_progress(self, request, queryset):
        """
        Admin action to mark selected orders as in progress.

        Args:
            request: The HTTP request object.
            queryset: QuerySet of selected Order objects.
        """
        updated = queryset.update(status="in_progress")
        self.message_user(
            request, f"{updated} order(s) marked as in progress."
        )

    mark_as_in_progress.short_description = (
        "Mark selected orders as in progress"
    )
