from django.contrib.auth.models import User
from django.db import models

from offers_app.models import Offer


# Create your models here.
class Order(models.Model):
    class Type(models.TextChoices):
        IN_PROGRESS = "in_progress", "in_progress"
        DELETED = "deleted", "deleted"
        CANCELLED = "cancelled", "cancelled"

    offer = models.ForeignKey(
        Offer, on_delete=models.CASCADE, related_name="orders"
    )

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        default="in_progress", blank=True, max_length=11, choices=Type.choices
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
