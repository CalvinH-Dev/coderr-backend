from django.urls import reverse
from rest_framework import serializers

from auth_app.api.serializers import UserDetailsSerializer
from offers_app.models import Offer, OfferPackage


class BaseOfferSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="offer-detail",
        read_only=True,
    )

    class Meta:
        model = Offer
        fields = [
            "id",
            "url",
        ]


class BaseOfferSerializerShortURL(BaseOfferSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta(BaseOfferSerializer.Meta):
        model = Offer
        fields = BaseOfferSerializer.Meta.fields + []

    def get_url(self, obj):
        url = reverse("offer-detail", kwargs={"pk": obj.pk})
        return url.removeprefix("/api")


class RetrieveOfferSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            "id",
            "title",
            # "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        ]

    def get_price(self, obj):
        price = obj.price
        return int(price) if price % 1 == 0 else price


class BaseOfferPackageSerializer(serializers.ModelSerializer):
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = OfferPackage
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "min_price",
            "min_delivery_time",
        ]

    def get_min_price(self, obj):
        offers = obj.offers.all()
        if not offers:
            return None
        min_price = min(offer.price for offer in offers)
        return int(min_price) if min_price % 1 == 0 else min_price

    def get_min_delivery_time(self, obj):
        offers = obj.offers.all()
        if not offers:
            return None
        return min(offer.delivery_time_in_days for offer in offers)


class ListOfferPackageSerializer(BaseOfferPackageSerializer):
    details = BaseOfferSerializerShortURL(
        many=True, source="offers", read_only=True
    )
    user_details = UserDetailsSerializer(source="user", read_only=True)

    class Meta(BaseOfferPackageSerializer.Meta):
        fields = BaseOfferPackageSerializer.Meta.fields + [
            "details",
            "user_details",
        ]


class RetrieveOfferPackageSerializer(BaseOfferPackageSerializer):
    details = BaseOfferSerializer(many=True, source="offers", read_only=True)

    class Meta(BaseOfferPackageSerializer.Meta):
        fields = BaseOfferPackageSerializer.Meta.fields + ["details"]
