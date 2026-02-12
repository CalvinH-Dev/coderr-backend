from rest_framework.authtoken.admin import User
from rest_framework.test import APITestCase

from auth_app.models import UserProfile
from offers_app.models import Offer, OfferPackage
from orders_app.models import Order


class TestDataFactory:
    @staticmethod
    def create_authenticated_client(
        username="testuser",
        email="test@example.com",
        first_name="Max",
        last_name="Mustermann",
        password="testpass123",
        **kwargs,
    ):
        from rest_framework.test import APIClient

        client = APIClient()
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            **kwargs,
        )

        client.force_authenticate(user=user)
        return client, user

    @staticmethod
    def authenticate_user(user):
        from rest_framework.test import APIClient

        client = APIClient()
        client.force_authenticate(user=user)
        return client
