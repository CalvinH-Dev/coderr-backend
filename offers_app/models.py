from django.db import models

from auth_app.models import UserProfile


class OfferPackage(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.FileField(upload_to="", blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Offer(models.Model):
    class Type(models.TextChoices):
        BASIC = "basic", "basic"
        STANDARD = "standard", "standard"
        PREMIUM = "premium", "premium"

    title = models.CharField(max_length=255)
    delivery_time_in_days = models.IntegerField()
    offer_type = models.CharField(max_length=8, choices=Type.choices)
    price = models.IntegerField(blank=True, null=True)
    features = models.JSONField(default=list, blank=True)
    package = models.ForeignKey(
        OfferPackage, on_delete=models.CASCADE, related_name="offers"
    )
