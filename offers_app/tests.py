from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.admin import User
from rest_framework.test import APITestCase

from core.test_factory.authenticate import TestDataFactory
from core.test_factory.data import APITestCaseWithSetup
from offers_app.models import Offer, OfferPackage


class TestOfferPackageViewSet(APITestCaseWithSetup):
    def setUp(self):
        self.client = TestDataFactory.authenticate_user(self.business_user_1)

    def test_offer_retrieve_ok(self):
        url = reverse(
            "offerpackage-detail", kwargs={"pk": self.offer_package_1.pk}
        )
        response = self.client.get(url)

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.pop("id"), self.offer_package_1.id)
        self.assertEqual(data.pop("user"), self.offer_package_1.user.id)
        self.assertEqual(data.pop("title"), self.offer_package_1.title)
        self.assertEqual(
            data.pop("description"), self.offer_package_1.description
        )
        self.assertEqual(data.pop("image"), self.offer_package_1.image)
        self.assertEqual(data.pop("min_price"), 100)
        self.assertEqual(data.pop("min_delivery_time"), 5)
        self.assertEqual(len(data.pop("details")), 3)
        self.assertIsNotNone(data.pop("created_at"))
        self.assertIsNotNone(data.pop("updated_at"))
        self.assertEqual(data, {}, f"Unexpected fields in response: {data}")

    def test_offer_retrieve_wrong_id(self):
        url = reverse("offerpackage-detail", kwargs={"pk": 999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_offer_retrieve_not_authorized(self):
        self.client.force_authenticate(user=None)
        url = reverse(
            "offerpackage-detail", kwargs={"pk": self.offer_package_1.pk}
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offer_list_ok(self):
        self.client.force_authenticate(user=None)
        url = reverse("offerpackage-list")
        response = self.client.get(url)

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.pop("count"), 2)
        self.assertEqual(data.pop("next"), None)
        self.assertEqual(data.pop("previous"), None)
        result_data = data.pop("results")[0]
        self.assertEqual(result_data.pop("id"), self.offer_package_2.id)
        self.assertEqual(result_data.pop("user"), self.business_user_2.id)
        self.assertEqual(result_data.pop("title"), "Graphic Design Package")
        self.assertEqual(
            result_data.pop("description"), self.offer_package_2.description
        )
        self.assertEqual(result_data.pop("image"), self.offer_package_2.image)
        self.assertEqual(result_data.pop("min_price"), 80)
        self.assertEqual(result_data.pop("min_delivery_time"), 3)
        self.assertEqual(
            result_data.pop("details"),
            [
                {"id": 4, "url": "/offerdetails/4/"},
                {"id": 5, "url": "/offerdetails/5/"},
                {"id": 6, "url": "/offerdetails/6/"},
            ],
        )

        self.assertEqual(
            result_data.pop("user_details"),
            {
                "first_name": "Sarah",
                "last_name": "Miller",
                "username": "sarah_miller",
            },
        )
        self.assertIsNotNone(result_data.pop("created_at"))
        self.assertIsNotNone(result_data.pop("updated_at"))
        self.assertEqual(
            result_data, {}, f"Unexpected fields in response: {result_data}"
        )
        self.assertEqual(data, {}, f"Unexpected fields in response: {data}")

    def test_offer_list_filter_by_creator_id_1(self):
        self.client.force_authenticate(user=None)
        url = (
            reverse("offerpackage-list")
            + f"?creator_id={self.business_user_1.id}"
        )
        response = self.client.get(url)

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 1)

    def test_offer_list_filter_by_creator_id_2(self):
        self.client.force_authenticate(user=None)
        url = (
            reverse("offerpackage-list")
            + f"?creator_id={self.business_user_2.id}"
        )
        response = self.client.get(url)

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 1)

    def test_offer_list_filter_by_min_price(self):
        self.client.force_authenticate(user=None)
        url = reverse("offerpackage-list") + "?min_price=85"
        response = self.client.get(url)

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 2)

    def test_offer_list_filter_by_search(self):
        self.client.force_authenticate(user=None)
        url = reverse("offerpackage-list") + "?search=Graphic"
        response = self.client.get(url)

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 1)

    def test_offer_list_filter_by_max_delivery_time(self):
        self.client.force_authenticate(user=None)
        url = reverse("offerpackage-list") + "?max_delivery_time=5"
        response = self.client.get(url)

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 2)

    def test_offer_list_order_by_min_price(self):
        self.client.force_authenticate(user=None)
        url = reverse("offerpackage-list") + "?ordering=min_price"
        response = self.client.get(url)

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 2)
        self.assertEqual(data["results"][0]["id"], self.offer_package_2.id)
        self.assertEqual(data["results"][1]["id"], self.offer_package_1.id)

    def test_offer_list_order_by_updated_at(self):
        self.client.force_authenticate(user=None)
        url = reverse("offerpackage-list") + "?ordering=updated_at"
        response = self.client.get(url)

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["results"][0]["id"], 2)
        self.assertEqual(data["results"][1]["id"], 1)

    def test_offer_create_ok(self):
        offer = {
            "title": "Graphics Package",
            "image": None,
            "description": "A comprehensive graphics package for businesses.",
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": ["Logo Design", "Business Card"],
                    "offer_type": "basic",
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": ["Logo Design", "Business Card", "Letterhead"],
                    "offer_type": "standard",
                },
                {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": [
                        "Logo Design",
                        "Business Card",
                        "Letterhead",
                        "Flyer",
                    ],
                    "offer_type": "premium",
                },
            ],
        }

        url = reverse("offerpackage-list")
        response = self.client.post(url, offer, format="json")

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data["title"], "Graphics Package")
        self.assertEqual(data["description"], offer.get("description"))
        self.assertEqual(len(data["details"]), 3)
        self.assertEqual(OfferPackage.objects.all().count(), 3)

    def test_offer_create_wrong_offer_len(self):
        offer = {
            "title": "Graphics Package",
            "image": None,
            "description": "A comprehensive graphics package for businesses.",
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": ["Logo Design", "Business Card"],
                    "offer_type": "basic",
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": ["Logo Design", "Business Card", "Letterhead"],
                    "offer_type": "standard",
                },
            ],
        }

        url = reverse("offerpackage-list")
        response = self.client.post(url, offer, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_offer_create_not_business_user(self):
        self.client = TestDataFactory.authenticate_user(self.customer_user_1)
        url = reverse("offerpackage-list")
        offer = {
            "title": "Graphics Package",
            "image": None,
            "description": "A comprehensive graphics package for businesses.",
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": ["Logo Design", "Business Card"],
                    "offer_type": "basic",
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": ["Logo Design", "Business Card", "Letterhead"],
                    "offer_type": "standard",
                },
                {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": [
                        "Logo Design",
                        "Business Card",
                        "Letterhead",
                        "Flyer",
                    ],
                    "offer_type": "premium",
                },
            ],
        }
        response = self.client.post(url, offer, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_offer_update_ok(self):
        url = reverse(
            "offerpackage-detail", kwargs={"pk": self.offer_package_1.pk}
        )
        patch_data = {
            "title": "Updated Graphics Package",
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

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["title"], patch_data.get("title"))
        self.assertEqual(len(data["details"]), 3)

    def test_offer_update_not_offer_owner(self):
        self.client = TestDataFactory.authenticate_user(self.business_user_2)
        url = reverse(
            "offerpackage-detail", kwargs={"pk": self.offer_package_1.pk}
        )
        patch_data = {
            "title": "Updated Graphics Package",
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

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_offer_delete_ok(self):
        self.business_user_1.is_staff = True
        self.business_user_1.is_superuser = True
        self.business_user_1.save()
        url = reverse(
            "offerpackage-detail", kwargs={"pk": self.offer_package_1.pk}
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(response.data)
        self.assertFalse(
            OfferPackage.objects.filter(pk=self.offer_package_1.pk).exists()
        )

    def test_offer_delete_forbidden(self):
        url = reverse(
            "offerpackage-detail", kwargs={"pk": self.offer_package_1.pk}
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestOfferDetailsView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="john_doe",
            email="john@example.com",
            first_name="John",
            last_name="Doe",
            password="testpass123",
        )
        cls.offer_package = OfferPackage.objects.create(
            user=cls.user, title="Package Title"
        )
        cls.offer = Offer.objects.create(
            title="Offer Title",
            delivery_time_in_days=5,
            revisions=5,
            price=10,
            offer_type="basic",
            features=["WebDev", "Other"],
            package=cls.offer_package,
        )

    def setUp(self):
        self.client = TestDataFactory.authenticate_user(self.user)

    def test_offer_detail_ok(self):
        url = reverse("offer-detail", kwargs={"pk": self.offer.pk})
        response = self.client.get(url)

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.pop("id"), self.offer.id)
        self.assertEqual(data.pop("title"), self.offer.title)
        self.assertEqual(data.pop("revisions"), self.offer.revisions)
        self.assertEqual(
            data.pop("delivery_time_in_days"), self.offer.delivery_time_in_days
        )
        self.assertEqual(data.pop("offer_type"), self.offer.offer_type)
        self.assertEqual(data.pop("price"), self.offer.price)
        self.assertEqual(data.pop("features"), self.offer.features)
        self.assertEqual(data, {}, f"Unexpected fields in response: {data}")
