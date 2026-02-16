from django.contrib.auth.models import User
from django.db import models

from offers_app.models import BaseOffer


class Order(BaseOffer):
    """
    Model representing a customer order based on an offer.

    Extends BaseOffer to create concrete order instances that track the
    relationship between business users and customer users. Each order
    maintains status information and timestamps for creation and updates.

    Attributes:
        business_user (User): The business user fulfilling the order.
        customer_user (User): The customer user who placed the order.
        status (str): Current status of the order (in_progress, cancelled,
            or completed).
        created_at (datetime): Timestamp when the order was created.
        updated_at (datetime): Timestamp when the order was last updated.
            Inherits all attributes from BaseOffer (title, revisions,
            delivery_time_in_days, offer_type, price, features).
    """

    class StatusType(models.TextChoices):
        """
        Predefined status choices for an order.

        IN_PROGRESS: Order is currently being worked on.
        CANCELLED: Order has been cancelled.
        COMPLETED: Order has been completed successfully.
        """

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
