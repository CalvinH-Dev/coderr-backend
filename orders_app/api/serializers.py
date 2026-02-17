from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from offers_app.api.serializers import PriceField
from offers_app.models import Offer
from orders_app.models import Order


class BaseOrderSerialier(serializers.ModelSerializer):
    """
    Base serializer for order objects.

    Provides common fields for order serialization with read-only offer
    details. This serializer is used as a base for concrete order serializers.

    Attributes:
        title (str): Read-only title copied from the offer.
        revisions (int): Read-only number of revisions from the offer.
        delivery_time_in_days (int): Read-only delivery time from the offer.
        price (Decimal): Read-only price from the offer.
        features (list): Read-only list of features from the offer.
        offer_type (str): Read-only offer type from the offer.
    """

    title = serializers.CharField(read_only=True)
    revisions = serializers.IntegerField(read_only=True)
    delivery_time_in_days = serializers.IntegerField(read_only=True)
    price = PriceField(max_digits=10, decimal_places=2, read_only=True)
    features = serializers.JSONField(read_only=True)
    offer_type = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_user",
            "business_user",
            "status",
            "created_at",
            "updated_at",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        ]

        extra_kwargs = {
            "business_user": {"read_only": True},
            "customer_user": {"read_only": True},
        }

        read_only_fields = ["created_at", "updated_at"]


class PatchOrderSerializer(BaseOrderSerialier):
    """
    Serializer for partially updating order status.

    Extends BaseOrderSerialier to allow only the status field to be updated.
    All other fields are read-only to prevent modification after order creation.
    """

    class Meta(BaseOrderSerialier.Meta):
        model = Order
        fields = BaseOrderSerialier.Meta.fields + []
        read_only_fields = [
            field
            for field in BaseOrderSerialier.Meta.fields
            if field != "status"
        ]


class CreateOrderSerializer(BaseOrderSerialier):
    """
    Serializer for creating new orders.

    Handles order creation by accepting an offer ID and automatically
    populating order details from the referenced offer. The customer user
    is automatically set to the authenticated user.

    Additional Fields:
        offer_detail_id (int): Write-only ID of the offer to order.
        user (User): Hidden field auto-populated with current user.
    """

    offer_detail_id = serializers.IntegerField(write_only=True)

    user = serializers.HiddenField(
        default=CurrentUserDefault(), write_only=True
    )

    class Meta(BaseOrderSerialier.Meta):
        model = Order
        fields = BaseOrderSerialier.Meta.fields + [
            "offer_detail_id",
            "user",
        ]
        read_only_fields = [
            field
            for field in BaseOrderSerialier.Meta.fields
            if field != "offer_detail_id"
        ]

    def create(self, validated_data):
        """Create an Order by populating fields from the referenced Offer."""
        offer_id = validated_data.pop("offer_detail_id", None)
        user = validated_data.pop("user")
        offer = Offer.objects.filter(id=offer_id).first()
        if not offer:
            raise serializers.ValidationError(
                {"offer_detail_id": "Offer not found"}
            )

        validated_data["title"] = offer.title
        validated_data["revisions"] = offer.revisions
        validated_data["delivery_time_in_days"] = offer.delivery_time_in_days
        validated_data["price"] = offer.price
        validated_data["features"] = offer.features
        validated_data["offer_type"] = offer.offer_type
        validated_data["business_user"] = offer.package.user

        return Order.objects.create(**validated_data, customer_user=user)
