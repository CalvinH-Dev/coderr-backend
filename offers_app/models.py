from django.db import models
from rest_framework.authtoken.admin import User


class BaseOffer(models.Model):
    class Type(models.TextChoices):
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.FileField(upload_to="", blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Offer(BaseOffer):
    package = models.ForeignKey(
        OfferPackage, on_delete=models.CASCADE, related_name="offers"
    )
