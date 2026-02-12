from django.contrib.auth.models import User
from django.db import models
from rest_framework.fields import MaxValueValidator, MinValueValidator

# Create your models here.


class Review(models.Model):
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
