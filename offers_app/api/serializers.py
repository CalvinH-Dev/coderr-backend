from rest_framework import serializers

from offers_app.models import Offer, OfferPackage


class BaseOfferSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="offer-detail",
        read_only=True,
    )

    class Meta:
        model = Offer
        fields = ["id", "url"]


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


class BaseOfferPackageSerializer(serializers.ModelSerializer):
    details = BaseOfferSerializer(many=True, source="offers", read_only=True)

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
        ]
