from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """
    Extended user profile model for storing additional user information.

    This model provides a one-to-one relationship with Django's User model
    and stores additional profile information such as contact details,
    account type, and business-specific fields.

    Attributes:
        user (User): One-to-one relationship with Django User model.
        location (str): User's location or address.
        tel (str): User's telephone number.
        type (str): Account type (customer or business).
        description (str): User or business description.
        file (FileField): Profile picture or business logo.
        working_hours (str): Business working hours (for business accounts).
        created_at (datetime): Timestamp when the profile was created.
    """

    class Type(models.TextChoices):
        """
        Predefined priority options for a user profile.

        CUSTOMER: Regular customer account with standard features.
        BUSINESS: Business account with extended features and priority support.
        """

        CUSTOMER = "customer", "Customer"
        BUSINESS = "business", "Business"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, blank=True, default="")
    tel = models.CharField(max_length=20, blank=True, default="")
    type = models.CharField(max_length=8, choices=Type.choices)
    description = models.CharField(max_length=255, blank=True, default="")
    file = models.FileField(upload_to="", blank=True, null=True)
    working_hours = models.CharField(max_length=20, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}"
