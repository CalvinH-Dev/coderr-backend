from django.db.models import Avg

from auth_app.models import UserProfile
from offers_app.models import OfferPackage
from reviews_app.models import Review


def get_review_count():
    """Return the total number of reviews."""
    return Review.objects.all().count()


def get_average_rating():
    """Return the average rating across all reviews."""
    reviews = Review.objects.all()
    average_rating = reviews.aggregate(Avg("rating"))
    return average_rating["rating__avg"]


def get_business_profile_count():
    """Return the total number of business user profiles."""
    users = UserProfile.objects.all()
    return users.filter(type="business").count()


def get_offer_count():
    """Return the total number of offer packages."""
    return OfferPackage.objects.all().count()
