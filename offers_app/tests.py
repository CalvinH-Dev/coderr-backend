from django.http import HttpResponse
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.admin import User
from rest_framework.test import APITestCase

from auth_app.models import UserProfile
from core.test_factory.authenticate import TestDataFactory
from offers_app.models import Offer, OfferPackage


class TestOfferPackageViewSet(APITestCase):
    def setUp(self):
        self.client, self.user = TestDataFactory.create_authenticated_client(
            username="john_doe",
            email="john@example.com",
            first_name="John",
            last_name="Doe",
        )
        self.offer_package = OfferPackage.objects.create(
            user=self.user, title="Package Title"
        )
        Offer.objects.create(
            title="Offer Title",
            delivery_time_in_days=5,
            price=10,
            offer_type="basic",
            features=["WebDev", "Anderes"],
            package=self.offer_package,
        )
        Offer.objects.create(
            title="Offer Title",
            delivery_time_in_days=10,
            price=20,
            offer_type="basic",
            features=["WebDev", "Anderes"],
            package=self.offer_package,
        )

    def test_offer_retrieve_ok(self):
        url = reverse("offerpackage-detail", None, kwargs={"pk": 1})
        response: HttpResponse = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["user"], self.offer_package.user.id)  # type: ignore
        self.assertEqual(data["title"], self.offer_package.title)
        self.assertEqual(data["description"], self.offer_package.description)
        self.assertEqual(data["image"], self.offer_package.image)
        self.assertEqual(data["min_price"], 10)
        self.assertEqual(data["min_delivery_time"], 5)

        self.assertIsNotNone(data["created_at"])
        self.assertIsNotNone(data["updated_at"])

    def test_offer_retrieve_wrong_id(self):
        url = reverse("offerpackage-detail", None, kwargs={"pk": 999})
        response: HttpResponse = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_offer_retrieve_not_authenticated(self):
        self.client.force_authenticate(user=None)  # type: ignore
        url = reverse("offerpackage-detail", None, kwargs={"pk": 1})
        response: HttpResponse = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offer_list_ok(self):
        self.client.force_authenticate(user=None)  # type: ignore
        url = reverse("offerpackage-list")
        response: HttpResponse = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()[0]
        self.assertEqual(data["user"], self.offer_package.user.id)  # type: ignore
        self.assertEqual(data["title"], self.offer_package.title)
        self.assertEqual(data["description"], self.offer_package.description)
        self.assertEqual(data["image"], self.offer_package.image)
        self.assertEqual(data["min_price"], 10)
        self.assertEqual(data["min_delivery_time"], 5)
        self.assertEqual(
            data["user_details"],
            {"first_name": "John", "last_name": "Doe", "username": "john_doe"},
        )
        self.assertEqual(
            data["details"],
            [
                {"id": 1, "url": "/offerdetails/1/"},
                {"id": 2, "url": "/offerdetails/2/"},
            ],
        )

        self.assertIsNotNone(data["created_at"])
        self.assertIsNotNone(data["updated_at"])


class TestOfferDetailsView(APITestCase):
    def setUp(self):
        self.client, self.user = TestDataFactory.create_authenticated_client(
            username="john_doe",
            email="john@example.com",
            first_name="John",
            last_name="Doe",
        )

        self.offer_package = OfferPackage.objects.create(
            user=self.user, title="Package Title"
        )
        self.offer = Offer.objects.create(
            title="Offer Title",
            delivery_time_in_days=5,
            price=10,
            offer_type="basic",
            features=["WebDev", "Anderes"],
            package=self.offer_package,
        )

    def test_offer_detail_ok(self):
        url = reverse("offer-detail", None, kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["id"], self.offer.id)  # type: ignore
        self.assertEqual(data["title"], self.offer.title)
        self.assertEqual(
            data["delivery_time_in_days"], self.offer.delivery_time_in_days
        )
        self.assertEqual(data["offer_type"], self.offer.offer_type)
        self.assertEqual(data["price"], self.offer.price)
        self.assertEqual(data["features"], self.offer.features)
