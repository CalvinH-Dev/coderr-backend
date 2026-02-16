from django.urls import reverse
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from auth_app.api.serializers import UserDetailsSerializer
from offers_app.models import Offer, OfferPackage


class PriceField(serializers.DecimalField):
    """
    Custom decimal field for price representation.

    Converts decimal prices to integers when the value is a whole number,
    otherwise returns as float.
    """

    def to_representation(self, value):
        value = super().to_representation(value)
        if value is not None and float(value) == int(float(value)):
            return int(float(value))
        return float(value)


class BaseOfferSerializer(serializers.ModelSerializer):
    """
    Base serializer for offer objects.

    Provides basic offer information with a hyperlinked URL to the
    offer detail endpoint.
    """

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
    """
    Base offer serializer with shortened URL format.

    Extends BaseOfferSerializer to provide URLs without the '/api' prefix
    for cleaner frontend routing.
    """

    url = serializers.SerializerMethodField(read_only=True)

    class Meta(BaseOfferSerializer.Meta):
        model = Offer
        fields = BaseOfferSerializer.Meta.fields + []

    def get_url(self, obj):
        """
        Generate a shortened URL for the offer detail endpoint.

        Args:
            obj (Offer): The offer instance.

        Returns:
            str: URL path with '/api' prefix removed.
        """
        url = reverse("offer-detail", kwargs={"pk": obj.pk})
        return url.removeprefix("/api")


class CreateOrUpdateOfferSerializer(serializers.ModelSerializer):
    """
    Serializer for creating or updating individual offers.

    Handles offer data input including title, pricing, delivery time,
    and features.
    """

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
    """
    Serializer for retrieving offer details.

    Provides read-only representation of offer data with formatted
    price display.
    """

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
        """
        Format the price for display.

        Args:
            obj (Offer): The offer instance.

        Returns:
            int or Decimal: Integer if price is whole number, Decimal otherwise.
        """
        price = obj.price
        return int(price) if price % 1 == 0 else price


class BaseOfferPackageSerializer(serializers.ModelSerializer):
    """
    Base serializer for offer packages.

    Provides common fields for offer package serialization including
    calculated minimum price and delivery time from associated offers.
    """

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

        read_only_fields = ["created_at", "updated_at"]


class ListOfferPackageSerializer(BaseOfferPackageSerializer):
    """
    Serializer for listing offer packages.

    Extends BaseOfferPackageSerializer with nested offer details and
    user information for list views.
    """

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
    """
    Serializer for retrieving a single offer package.

    Extends BaseOfferPackageSerializer with nested offer details for
    detailed package view.
    """

    details = BaseOfferSerializer(many=True, source="offers", read_only=True)

    class Meta(BaseOfferPackageSerializer.Meta):
        fields = BaseOfferPackageSerializer.Meta.fields + ["details"]


class BaseCreateOrUpdateOfferPackageSerialier(serializers.ModelSerializer):
    """
    Base serializer for creating or updating offer packages.

    Provides common functionality for handling offer package data with
    nested offer creation/updates. The user field is automatically set
    to the current authenticated user.
    """

    user = serializers.HiddenField(
        default=CurrentUserDefault(), write_only=True
    )
    image = serializers.ImageField(required=False, allow_null=True)
    details = CreateOrUpdateOfferSerializer(many=True, source="offers")

    class Meta:
        model = OfferPackage
        fields = ["id", "user", "title", "image", "description", "details"]


class CreateOfferPackageSerializer(BaseCreateOrUpdateOfferPackageSerialier):
    """
    Serializer for creating new offer packages.

    Validates that exactly three offers (basic, standard, premium) are
    provided and creates the offer package with associated offers.
    """

    class Meta(BaseCreateOrUpdateOfferPackageSerialier.Meta):
        model = OfferPackage
        fields = BaseCreateOrUpdateOfferPackageSerialier.Meta.fields + []

    def validate_details(self, value):
        if len(value) != 3:
            raise serializers.ValidationError(
                "Exactly 3 offers (basic, standard, premium) must be provided."
            )
        return value

    def validate(self, data):
        offers = data.get("offers", [])

        if len(offers) != 3:
            raise serializers.ValidationError(
                {"details": "Exactly 3 offers must be provided."}
            )

        offer_types = {offer.get("offer_type") for offer in offers}
        required_types = {"basic", "standard", "premium"}

        if offer_types != required_types:
            missing = required_types - offer_types
            extra = offer_types - required_types
            error_msg = []

            if missing:
                error_msg.append(f"Missing types: {', '.join(missing)}")
            if extra:
                error_msg.append(f"Invalid types: {', '.join(extra)}")

            raise serializers.ValidationError(
                {"details": " ".join(error_msg) or "Invalid offer_types"}
            )

        return data

    def create(self, validated_data):
        offers_data = validated_data.pop("offers", None)

        offer_package = OfferPackage.objects.create(**validated_data)

        for offer_data in offers_data:
            Offer.objects.create(package=offer_package, **offer_data)

        return offer_package


class UpdateOfferPackageSerializer(BaseCreateOrUpdateOfferPackageSerialier):
    """
    Serializer for updating existing offer packages.

    Updates the offer package and its associated offers by matching
    offers based on their offer_type.
    """

    class Meta(BaseCreateOrUpdateOfferPackageSerialier.Meta):
        model = OfferPackage
        fields = BaseCreateOrUpdateOfferPackageSerialier.Meta.fields + []

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
