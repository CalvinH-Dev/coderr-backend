from django.db import models
from rest_framework.authtoken.admin import User


class BaseOffer(models.Model):
    """
    Abstract base model for offer objects.

    Provides common fields for all offer types including pricing, delivery
    time, revisions, and features. This model is not instantiated directly
    but serves as a base for concrete offer models.

    Attributes:
        title (str): The title or name of the offer.
        revisions (int): Number of revisions included in the offer.
        delivery_time_in_days (int): Expected delivery time in days.
        offer_type (str): Type of offer (basic, standard, or premium).
        price (float): Price of the offer.
        features (list): List of features included in the offer.
    """

    class Type(models.TextChoices):
        """
        Predefined offer type choices.

        BASIC: Entry-level offer with basic features.
        STANDARD: Mid-tier offer with additional features.
        PREMIUM: Top-tier offer with all features and benefits.
        """

        BASIC = "basic", "basic"
        STANDARD = "standard", "standard"
        PREMIUM = "premium", "premium"

    title = models.CharField(max_length=255)
    revisions = models.IntegerField(blank=True, null=True)
    delivery_time_in_days = models.IntegerField()
    offer_type = models.CharField(max_length=8, choices=Type.choices)
    price = models.FloatField(blank=True, null=True)
    features = models.JSONField(default=list, blank=True)

    class Meta:
        abstract = True


class OfferPackage(models.Model):
    """
    Model representing a package of related offers.

    An offer package groups together multiple offers (typically basic,
    standard, and premium tiers) under a single service offering. Each
    package is associated with a business user.

    Attributes:
        user (User): The business user who created this offer package.
        title (str): The title or name of the offer package.
        image (FileField): Optional image representing the offer package.
        description (str): Description of the offer package.
        created_at (datetime): Timestamp when the package was created.
        updated_at (datetime): Timestamp when the package was last updated.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.FileField(upload_to="", blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Offer(BaseOffer):
    """
    Model representing an individual offer within an offer package.

    Extends BaseOffer to create concrete offer instances that belong to
    an offer package. Each offer represents a specific tier (basic,
    standard, or premium) of service.

    Attributes:
        package (OfferPackage): The offer package this offer belongs to.
            Inherits all attributes from BaseOffer.
    """

    package = models.ForeignKey(
        OfferPackage, on_delete=models.CASCADE, related_name="offers"
    )
