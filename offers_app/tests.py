from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.admin import User
from rest_framework.test import APITestCase

from auth_app.models import UserProfile
from core.test_factory.authenticate import TestDataFactory
from offers_app.models import Offer, OfferPackage


class TestOfferPackageViewSet(APITestCase):
    def setUp(self):
        self.user_data = {
            "username": "exampleUsername",
            "password": "examplePassword",
        }
        self.user = User.objects.create_user(
            email="example@mail.de",
            **self.user_data,
        )
        user_profile = UserProfile.objects.create(
            user=self.user, type="customer"
        )
        self.offer_package = OfferPackage.objects.create(
            user=user_profile, title="Package Title"
        )
        offer = Offer.objects.create(
            title="Offer Title",
            delivery_time_in_days=5,
            offer_type="basic",
            features=["WebDev", "Anderes"],
            package=self.offer_package,
        )

    def test_offers_list_ok(self):
        url = reverse("offers-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["user"], self.offer_package.user.id)
        self.assertEqual(response.data[0]["title"], self.offer_package.title)
        self.assertEqual(
            response.data[0]["description"], self.offer_package.description
        )
        self.assertEqual(response.data[0]["image"], self.offer_package.image)
        self.assertIsNotNone(response.data[0]["created_at"])
        self.assertIsNotNone(response.data[0]["updated_at"])


class TestOfferDetailsView(APITestCase):
    def setUp(self):
        self.client, self.user = TestDataFactory.create_authenticated_client(
            username="john_doe",
            email="john@example.com",
            first_name="John",
            last_name="Doe",
        )
        self.profile_data = {
            "file": "profile_picture.jpg",
            "location": "Berlin",
            "tel": "123456789",
            "description": "Business description",
            "working_hours": "9-17",
            "type": "business",
        }

        user_profile = UserProfile.objects.create(
            user=self.user, **self.profile_data
        )

        self.offer_package = OfferPackage.objects.create(
            user=user_profile, title="Package Title"
        )
        self.offer = Offer.objects.create(
            title="Offer Title",
            delivery_time_in_days=5,
            offer_type="basic",
            price=1.05,
            features=["WebDev", "Anderes"],
            package=self.offer_package,
        )

    def test_offer_detail_ok(self):
        url = reverse("offer-detail", None, kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.offer.id)
        self.assertEqual(response.data["title"], "Offer Title")
        self.assertEqual(response.data["delivery_time_in_days"], 5)
        self.assertEqual(response.data["offer_type"], "basic")
        self.assertEqual(response.data["price"], 1.05)
        self.assertEqual(response.data["features"], ["WebDev", "Anderes"])
