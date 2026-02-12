from django.contrib.auth.models import User
from django.db import models

from offers_app.models import BaseOffer


# Create your models here.
class Order(BaseOffer):
    class StatusType(models.TextChoices):
        IN_PROGRESS = "in_progress", "in_progress"
        CANCELLED = "cancelled", "cancelled"
        COMPLETED = "completed", "completed"

    business_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders_as_business"
    )
    customer_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders_as_customer"
    )
    status = models.CharField(
        default="in_progress",
        blank=True,
        max_length=11,
        choices=StatusType.choices,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
