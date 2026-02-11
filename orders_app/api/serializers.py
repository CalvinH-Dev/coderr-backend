from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from offers_app.api.serializers import RetrieveOfferSerializer
from offers_app.models import Offer
from orders_app.models import Order


class CreateOrderSerializer(serializers.ModelSerializer):
    offer = RetrieveOfferSerializer(read_only=True)
    offer_detail_id = serializers.IntegerField(write_only=True)
    user = serializers.HiddenField(
        default=CurrentUserDefault(), write_only=True
    )

    customer_user = serializers.SerializerMethodField(read_only=True)
    business_user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "offer_detail_id",
            "user",
            "customer_user",
            "business_user",
            "offer",
            "status",
            "created_at",
        ]

    def get_customer_user(self, obj):
        return obj.customer.id

    def get_business_user(self, obj):
        if obj.offer:
            return obj.offer.package.user.id
        return None

    def create(self, validated_data):
        offer_id = validated_data.pop("offer_detail_id", None)
        user = validated_data.pop("user")
        offer = Offer.objects.filter(id=offer_id).first()

        return Order.objects.create(
            **validated_data, offer=offer, customer=user
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if representation.get("offer"):
            offer_data = representation.pop("offer")
            offer_data.pop("id", None)
            representation.update(offer_data)

        return representation
