from django.contrib import admin

from auth_app.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for UserProfile model.

    Provides a comprehensive admin interface for managing user profiles
    with filtering, searching, and organized field display.
    """

    list_display = [
        "id",
        "user",
        "type",
        "location",
        "tel",
        "created_at",
    ]
    list_filter = ["type", "created_at", "location"]
    search_fields = ["user__username", "user__email", "tel", "description"]
    readonly_fields = ["created_at"]

    fieldsets = (
        ("User Information", {"fields": ("user", "type")}),
        ("Contact Details", {"fields": ("tel", "location")}),
        (
            "Profile Details",
            {"fields": ("description", "file", "working_hours")},
        ),
        ("Timestamps", {"fields": ("created_at",), "classes": ("collapse",)}),
    )

    list_per_page = 25
    ordering = ["-created_at"]
