from django.http import HttpResponse
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.admin import User
from rest_framework.test import APITestCase

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

        user_2 = User.objects.create(
            username="exampleUsername",
            email="username@example.com",
            first_name="Example",
            last_name="Username",
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
            title="Offer Title 2",
            delivery_time_in_days=10,
            price=20,
            offer_type="basic",
            features=["WebDev", "Anderes"],
            package=self.offer_package,
        )
        offer_package_2 = OfferPackage.objects.create(
            user=user_2, title="Advanced Title"
        )
        Offer.objects.create(
            title="Offer Title",
            delivery_time_in_days=3,
            price=35,
            offer_type="basic",
            features=["WebDev", "Anderes"],
            package=offer_package_2,
        )
        Offer.objects.create(
            title="Offer Title 2",
            delivery_time_in_days=15,
            price=50,
            offer_type="basic",
            features=["WebDev", "Anderes"],
            package=offer_package_2,
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
        data = response.json()
        self.assertEqual(data["count"], 2)
        self.assertEqual(data["next"], None)
        self.assertEqual(data["previous"], None)
        result_data = data["results"][0]
        self.assertEqual(result_data["user"], 2)  # type: ignore
        self.assertEqual(result_data["title"], "Advanced Title")
        self.assertEqual(
            result_data["description"], self.offer_package.description
        )
        self.assertEqual(result_data["image"], self.offer_package.image)
        self.assertEqual(result_data["min_price"], 35.0)
        self.assertEqual(result_data["min_delivery_time"], 3)
        self.assertEqual(
            result_data["user_details"],
            {
                "first_name": "Example",
                "last_name": "Username",
                "username": "exampleUsername",
            },
        )
        self.assertEqual(
            result_data["details"],
            [
                {"id": 3, "url": "/offerdetails/3/"},
                {"id": 4, "url": "/offerdetails/4/"},
            ],
        )

        self.assertIsNotNone(result_data["created_at"])
        self.assertIsNotNone(result_data["updated_at"])

    def test_offer_list_filtering(self):
        self.client.force_authenticate(user=None)  # type: ignore
        url_1 = reverse("offerpackage-list") + "?creator_id=1"
        url_2 = reverse("offerpackage-list") + "?creator_id=2"
        url_min_price = reverse("offerpackage-list") + "?min_price=25"
        url_search = reverse("offerpackage-list") + "?search=Advanced"
        response_1 = self.client.get(url_1)
        response_2 = self.client.get(url_2)
        response_min_price = self.client.get(url_min_price)
        response_search = self.client.get(url_search)
        self.assertEqual(response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(response_min_price.status_code, status.HTTP_200_OK)
        data_1 = response_1.json()
        data_2 = response_2.json()
        data_min_price = response_min_price.json()
        data_search = response_search.json()
        self.assertEqual(data_1["count"], 1)
        self.assertEqual(data_2["count"], 1)
        self.assertEqual(data_min_price["count"], 1)
        self.assertEqual(data_search["count"], 1)


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
