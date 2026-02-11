from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from offers_app.api.serializers import PriceField
from offers_app.models import Offer
from orders_app.models import Order


class CreateOrderSerializer(serializers.ModelSerializer):
    offer_detail_id = serializers.IntegerField(write_only=True)

    user = serializers.HiddenField(
        default=CurrentUserDefault(), write_only=True
    )

    customer_user = serializers.SerializerMethodField(read_only=True)
    business_user = serializers.SerializerMethodField(read_only=True)

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
            "offer_detail_id",
            "user",
            "customer_user",
            "business_user",
            "status",
            "created_at",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        ]

    def get_customer_user(self, obj):
        return obj.customer.id

    def get_business_user(self, obj):
        offer_id = self.initial_data.get("offer_detail_id")
        if offer_id:
            offer = Offer.objects.filter(id=offer_id).first()
            if offer:
                return offer.package.user.id
        return None

    def create(self, validated_data):
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

        return Order.objects.create(**validated_data, customer=user)
