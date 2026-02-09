from rest_framework import serializers

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


class RetrieveOfferSerializer(serializers.ModelSerializer):
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


class RetrieveOfferPackageSerializer(serializers.ModelSerializer):
    details = BaseOfferSerializer(many=True, source="offers", read_only=True)
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
            "details",
            "min_price",
            "min_delivery_time",
        ]

    def get_min_price(self, obj):
        offers = obj.offers.all()
        if not offers:
            return None
        return min(offer.price for offer in offers)

    def get_min_delivery_time(self, obj):
        offers = obj.offers.all()
        if not offers:
            return None
        return min(offer.delivery_time_in_days for offer in offers)
