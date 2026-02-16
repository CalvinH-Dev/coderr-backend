from django.contrib.auth.models import User
from django.db import models
from rest_framework.fields import MaxValueValidator, MinValueValidator


class Review(models.Model):
    """
    Model representing a user review for a business user.

    Allows customers to provide ratings and written feedback for business
    users. Each customer can only submit one review per business user,
    enforced by a database constraint.

    Attributes:
        business_user (User): The business user being reviewed.
        reviewer (User): The user who wrote the review.
        rating (int): Rating value between 1 and 5 (inclusive).
        description (str): Written review text (max 255 characters).
        created_at (datetime): Timestamp when the review was created.
        updated_at (datetime): Timestamp when the review was last updated.

    Constraints:
        unique_review_per_business_user: Ensures each reviewer can only
            submit one review per business user.
    """

    business_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_reviews"
    )

    reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="written_reviews"
    )

    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["business_user", "reviewer"],
                name="unique_review_per_business_user",
            )
        ]
