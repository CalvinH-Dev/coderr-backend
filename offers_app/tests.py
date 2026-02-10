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
        business_user = {
            "username": "john_doe",
            "email": "john@example.com",
            "first_name": "John",
            "last_name": "Doe",
        }
        self.client, self.user = TestDataFactory.create_authenticated_client(
            **business_user
        )

        self.business_user_profile = UserProfile.objects.create(
            user=self.user,
            type="business",
            tel="123456789",
            location="Berlin",
            description="Business User",
            file="laughing.jpg",
            working_hours="5-17",
        )

        business_user_2 = {
            "username": "sarah_miller",
            "email": "sarah.miller@example.com",
            "first_name": "Sarah",
            "last_name": "Miller",
        }

        self.business_user_2 = User.objects.create(**business_user_2)

        self.customer_user = User.objects.create(
            username="exampleUsername",
            email="username@example.com",
            first_name="Example",
            last_name="Username",
        )

        self.customer_user_profile = UserProfile.objects.create(
            user=self.customer_user,
            type="customer",
            tel="123456789",
            location="Berlin",
            description="Business User",
            file="laughing.jpg",
            working_hours="5-17",
        )

        self.offer_package = OfferPackage.objects.create(
            user=self.user, title="Package Title"
        )
        Offer.objects.create(
            title="Offer Title",
            delivery_time_in_days=5,
            revisions=5,
            price=10,
            offer_type="basic",
            features=["WebDev", "Anderes"],
            package=self.offer_package,
        )
        Offer.objects.create(
            title="Offer Title 2",
            delivery_time_in_days=10,
            revisions=3,
            price=20,
            offer_type="standard",
            features=["WebDev", "Anderes"],
            package=self.offer_package,
        )
        offer_package_2 = OfferPackage.objects.create(
            user=self.business_user_2, title="Advanced Title"
        )
        Offer.objects.create(
            title="Offer Title",
            delivery_time_in_days=3,
            revisions=2,
            price=35,
            offer_type="basic",
            features=["WebDev", "Anderes"],
            package=offer_package_2,
        )
        Offer.objects.create(
            title="Offer Title 2",
            delivery_time_in_days=15,
            revisions=10,
            price=50,
            offer_type="standard",
            features=["WebDev", "Anderes"],
            package=offer_package_2,
        )

    def test_offer_retrieve_ok(self):
        url = reverse("offerpackage-detail", None, kwargs={"pk": 1})
        response = self.client.get(url)
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
        print(result_data["min_price"])
        self.assertEqual(result_data["min_price"], 35)
        self.assertEqual(result_data["min_delivery_time"], 3)
        self.assertEqual(
            result_data["user_details"],
            {
                "first_name": "Sarah",
                "last_name": "Miller",
                "username": "sarah_miller",
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

    def test_offer_list_filter_by_creator_id_1(self):
        self.client.force_authenticate(user=None)  # type: ignore
        url = reverse("offerpackage-list") + "?creator_id=1"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 1)

    def test_offer_list_filter_by_creator_id_2(self):
        self.client.force_authenticate(user=None)  # type: ignore
        url = reverse("offerpackage-list") + "?creator_id=2"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 1)

    def test_offer_list_filter_by_min_price(self):
        self.client.force_authenticate(user=None)  # type: ignore
        url = reverse("offerpackage-list") + "?min_price=25"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 1)

    def test_offer_list_filter_by_search(self):
        self.client.force_authenticate(user=None)  # type: ignore
        url = reverse("offerpackage-list") + "?search=Advanced"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 1)

    def test_offer_list_filter_by_max_delivery_time(self):
        self.client.force_authenticate(user=None)  # type: ignore
        url = reverse("offerpackage-list") + "?max_delivery_time=5"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 2)

    def test_offer_list_order_by_min_price(self):
        self.client.force_authenticate(user=None)  # type: ignore
        url = reverse("offerpackage-list") + "?ordering=min_price"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 2)
        self.assertEqual(data["results"][0]["id"], 1)
        self.assertEqual(data["results"][1]["id"], 2)

    def test_offer_list_order_by_updated_at(self):
        self.client.force_authenticate(user=None)  # type: ignore
        url = reverse("offerpackage-list") + "?ordering=updated_at"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 2)
        self.assertEqual(data["results"][0]["id"], 2)
        self.assertEqual(data["results"][1]["id"], 1)

    def test_offer_create_ok(self):  # type: ignore
        offer = {
            "title": "Grafikdesign-Paket",
            "image": None,
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": ["Logo Design", "Visitenkarte"],
                    "offer_type": "basic",
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": ["Logo Design", "Visitenkarte", "Briefpapier"],
                    "offer_type": "standard",
                },
                {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": [
                        "Logo Design",
                        "Visitenkarte",
                        "Briefpapier",
                        "Flyer",
                    ],
                    "offer_type": "premium",
                },
            ],
        }

        url = reverse("offerpackage-list")
        response = self.client.post(url, offer, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        expected_data = {
            "id": 3,
            "title": "Grafikdesign-Paket",
            "image": None,
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
                {
                    "id": 5,
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": ["Logo Design", "Visitenkarte"],
                    "offer_type": "basic",
                },
                {
                    "id": 6,
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": ["Logo Design", "Visitenkarte", "Briefpapier"],
                    "offer_type": "standard",
                },
                {
                    "id": 7,
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": [
                        "Logo Design",
                        "Visitenkarte",
                        "Briefpapier",
                        "Flyer",
                    ],
                    "offer_type": "premium",
                },
            ],
        }
        data = response.json()
        self.assertEqual(data, expected_data)
        self.assertEqual(OfferPackage.objects.all().count(), 3)
        self.assertIsNotNone(
            OfferPackage.objects.all().filter(id=expected_data["id"]).first()
        )

    def test_offer_create_not_business_user(self):
        self.client = TestDataFactory.authenticate_user(self.customer_user)
        url = reverse("offerpackage-list")
        offer = {
            "title": "Grafikdesign-Paket",
            "image": None,
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": ["Logo Design", "Visitenkarte"],
                    "offer_type": "basic",
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": ["Logo Design", "Visitenkarte", "Briefpapier"],
                    "offer_type": "standard",
                },
                {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": [
                        "Logo Design",
                        "Visitenkarte",
                        "Briefpapier",
                        "Flyer",
                    ],
                    "offer_type": "premium",
                },
            ],
        }
        response = self.client.post(url, offer, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # type: ignore

    def test_offer_update_ok(self):
        url = reverse("offerpackage-detail", kwargs={"pk": 1})
        patch_data = {
            "title": "Updated Grafikdesign-Paket",
            "details": [
                {
                    "title": "Basic Design Updated",
                    "revisions": 3,
                    "delivery_time_in_days": 6,
                    "price": 120,
                    "features": ["Logo Design", "Flyer"],
                    "offer_type": "basic",
                }
            ],
        }
        response = self.client.patch(url, patch_data, format="json")
        expected_data = {
            "id": 1,
            "title": "Updated Grafikdesign-Paket",
            "image": None,
            "description": "",
            "details": [
                {
                    "id": 1,
                    "title": "Basic Design Updated",
                    "revisions": 3,
                    "delivery_time_in_days": 6,
                    "price": 120,
                    "features": ["Logo Design", "Flyer"],
                    "offer_type": "basic",
                },
                {
                    "id": 2,
                    "title": "Offer Title 2",
                    "revisions": 3,
                    "delivery_time_in_days": 10,
                    "price": 20,
                    "features": [
                        "WebDev",
                        "Anderes",
                    ],
                    "offer_type": "standard",
                },
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data, expected_data)

    def test_offer_update_not_offer_owner(self):
        self.client = TestDataFactory.authenticate_user(self.business_user_2)
        url = reverse("offerpackage-detail", kwargs={"pk": 1})
        patch_data = {
            "title": "Updated Grafikdesign-Paket",
            "details": [
                {
                    "title": "Basic Design Updated",
                    "revisions": 3,
                    "delivery_time_in_days": 6,
                    "price": 120,
                    "features": ["Logo Design", "Flyer"],
                    "offer_type": "basic",
                }
            ],
        }
        response = self.client.patch(url, patch_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # type: ignore


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
