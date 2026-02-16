from django.contrib import admin

from offers_app.models import Offer, OfferPackage


class OfferInline(admin.TabularInline):
    """
    Inline admin interface for Offer model within OfferPackage.

    Allows managing offers directly from the offer package admin page.
    """

    model = Offer
    extra = 0
    fields = [
        "offer_type",
        "title",
        "price",
        "delivery_time_in_days",
        "revisions",
    ]
    readonly_fields = []
    min_num = 3
    max_num = 3


@admin.register(OfferPackage)
class OfferPackageAdmin(admin.ModelAdmin):
    """
    Admin interface for OfferPackage model.

    Provides management interface for offer packages with inline offer
    editing and comprehensive filtering options.
    """

    list_display = [
        "id",
        "title",
        "user",
        "get_min_price",
        "get_min_delivery_time",
        "created_at",
        "updated_at",
    ]
    list_filter = ["created_at", "updated_at", "user"]
    search_fields = ["title", "description", "user__username"]
    readonly_fields = ["created_at", "updated_at"]
    inlines = [OfferInline]

    fieldsets = (
        (
            "Package Information",
            {"fields": ("user", "title", "description", "image")},
        ),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    list_per_page = 25
    ordering = ["-created_at"]

    def get_min_price(self, obj):
        """
        Get the minimum price from associated offers.

        Args:
            obj (OfferPackage): The offer package instance.

        Returns:
            float or str: Minimum price or 'N/A' if no offers exist.
        """
        prices = [offer.price for offer in obj.offers.all() if offer.price]
        return min(prices) if prices else "N/A"

    get_min_price.short_description = "Min Price"
    get_min_price.admin_order_field = "offers__price"

    def get_min_delivery_time(self, obj):
        """
        Get the minimum delivery time from associated offers.

        Args:
            obj (OfferPackage): The offer package instance.

        Returns:
            int or str: Minimum delivery time in days or 'N/A' if no offers exist.
        """
        times = [offer.delivery_time_in_days for offer in obj.offers.all()]
        return min(times) if times else "N/A"

    get_min_delivery_time.short_description = "Min Delivery (days)"


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    """
    Admin interface for individual Offer model.

    Provides detailed management interface for offers with filtering
    by type and package.
    """

    list_display = [
        "id",
        "title",
        "offer_type",
        "price",
        "delivery_time_in_days",
        "revisions",
        "package",
    ]
    list_filter = ["offer_type", "package__user"]
    search_fields = ["title", "package__title"]

    fieldsets = (
        ("Offer Details", {"fields": ("package", "title", "offer_type")}),
        (
            "Pricing & Delivery",
            {"fields": ("price", "delivery_time_in_days", "revisions")},
        ),
        ("Features", {"fields": ("features",)}),
    )

    list_per_page = 25
    ordering = ["package", "offer_type"]
