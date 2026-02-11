from django.urls import reverse
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from auth_app.api.serializers import UserDetailsSerializer
from offers_app.models import Offer, OfferPackage


class PriceField(serializers.DecimalField):
    def to_representation(self, value):
        value = super().to_representation(value)
        if value is not None and float(value) == int(float(value)):
            return int(float(value))
        return value


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


class CreateOrUpdateOfferSerializer(serializers.ModelSerializer):
    price = PriceField(max_digits=10, decimal_places=2)

    class Meta:
        model = Offer
        fields = [
            "id",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        ]


class RetrieveOfferSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            "id",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        ]

    def get_price(self, obj):
        price = obj.price
        return int(price) if price % 1 == 0 else price


class BaseOfferPackageSerializer(serializers.ModelSerializer):
    min_price = PriceField(max_digits=10, decimal_places=2)
    min_delivery_time = serializers.IntegerField()

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


class CreateOrUpdateOfferPackageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=CurrentUserDefault(), write_only=True
    )
    image = serializers.ImageField(required=False, allow_null=True)
    details = CreateOrUpdateOfferSerializer(many=True, source="offers")

    class Meta:
        model = OfferPackage
        fields = ["id", "user", "title", "image", "description", "details"]

    def create(self, validated_data):
        offers_data = validated_data.pop("offers", None)

        offer_package = OfferPackage.objects.create(**validated_data)

        for offer_data in offers_data:
            Offer.objects.create(package=offer_package, **offer_data)

        return offer_package

    def update(self, instance, validated_data):
        offer_data = validated_data.pop("offers", None)

        if offer_data:
            for updated_offer in offer_data:
                for offer in instance.offers.all():
                    if offer.offer_type == updated_offer.get("offer_type"):
                        for key, value in updated_offer.items():
                            setattr(offer, key, value)
                        offer.save()
                        break

        return super().update(instance, validated_data)
