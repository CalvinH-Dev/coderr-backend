from django.db.models import Avg

from auth_app.models import UserProfile
from offers_app.models import Offer
from reviews_app.models import Review


def get_review_count():
    return Review.objects.all().count()


def get_average_rating():
    reviews = Review.objects.all()
    average_rating = reviews.aggregate(Avg("rating"))
    return average_rating["rating__avg"]


def get_business_profile_count():
    users = UserProfile.objects.all()
    return users.filter(type="business").count()


def get_offer_count():
    return Offer.objects.all().count()
