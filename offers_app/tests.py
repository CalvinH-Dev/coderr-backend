import json

from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.admin import User
from rest_framework.test import APITestCase

from auth_app.models import UserProfile
from core.test_factory.authenticate import TestDataFactory
from offers_app.models import Offer, OfferPackage


class TestOfferPackageViewSet(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.business_user_1 = User.objects.create_user(
            username="john_doe",
            email="john@example.com",
            first_name="John",
            last_name="Doe",
            password="testpass123",
        )
        cls.business_profile_1 = UserProfile.objects.create(
            user=cls.business_user_1,
            type="business",
            tel="123456789",
            location="Berlin",
            description="Business User 1",
            file="laughing.jpg",
            working_hours="5-17",
        )
        cls.offer_package_1 = OfferPackage.objects.create(
            user=cls.business_user_1, title="Web Development Package"
        )
        Offer.objects.create(
            title="Basic Web Package",
            delivery_time_in_days=5,
            revisions=2,
            price=100,
            offer_type="basic",
            features=["WebDev", "Responsive"],
            package=cls.offer_package_1,
        )
        Offer.objects.create(
            title="Standard Web Package",
            delivery_time_in_days=10,
            revisions=5,
            price=250,
            offer_type="standard",
            features=["WebDev", "Responsive", "SEO"],
            package=cls.offer_package_1,
        )
        Offer.objects.create(
            title="Premium Web Package",
            delivery_time_in_days=15,
            revisions=10,
            price=500,
            offer_type="premium",
            features=["WebDev", "Responsive", "SEO", "Analytics"],
            package=cls.offer_package_1,
        )

        cls.business_user_2 = User.objects.create_user(
            username="sarah_miller",
            email="sarah.miller@example.com",
            first_name="Sarah",
            last_name="Miller",
            password="testpass123",
        )
        cls.business_profile_2 = UserProfile.objects.create(
            user=cls.business_user_2,
            type="business",
            tel="987654321",
            location="Munich",
            description="Business User 2",
            file="smiling.jpg",
            working_hours="9-18",
        )
        cls.offer_package_2 = OfferPackage.objects.create(
            user=cls.business_user_2, title="Graphic Design Package"
        )
        Offer.objects.create(
            title="Basic Design",
            delivery_time_in_days=3,
            revisions=1,
            price=80,
            offer_type="basic",
            features=["Logo", "Business Card"],
            package=cls.offer_package_2,
        )
        Offer.objects.create(
            title="Standard Design",
            delivery_time_in_days=7,
            revisions=3,
            price=200,
            offer_type="standard",
            features=["Logo", "Business Card", "Letterhead"],
            package=cls.offer_package_2,
        )
        Offer.objects.create(
            title="Premium Design",
            delivery_time_in_days=14,
            revisions=8,
            price=450,
            offer_type="premium",
            features=["Logo", "Business Card", "Letterhead", "Flyer"],
            package=cls.offer_package_2,
        )

        cls.customer_user_1 = User.objects.create_user(
            username="alice_customer",
            email="alice@example.com",
            first_name="Alice",
            last_name="Customer",
            password="testpass123",
        )
        cls.customer_profile_1 = UserProfile.objects.create(
            user=cls.customer_user_1,
            type="customer",
            tel="111222333",
            location="Hamburg",
            description="Customer User 1",
        )

        cls.customer_user_2 = User.objects.create_user(
            username="bob_customer",
            email="bob@example.com",
            first_name="Bob",
            last_name="Customer",
            password="testpass123",
        )
        cls.customer_profile_2 = UserProfile.objects.create(
            user=cls.customer_user_2,
            type="customer",
            tel="444555666",
            location="Frankfurt",
            description="Customer User 2",
        )

    def setUp(self):
        self.client = TestDataFactory.authenticate_user(self.business_user_1)

    def test_offer_retrieve_ok(self):
        url = reverse(
            "offerpackage-detail", kwargs={"pk": self.offer_package_1.pk}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["user"], self.offer_package_1.user.id)
        self.assertEqual(data["title"], self.offer_package_1.title)
        self.assertEqual(data["description"], self.offer_package_1.description)
        self.assertEqual(data["image"], self.offer_package_1.image)
        self.assertEqual(data["min_price"], 100)
        self.assertEqual(data["min_delivery_time"], 5)
        self.assertEqual(len(data["details"]), 3)
        self.assertIsNotNone(data["created_at"])
        self.assertIsNotNone(data["updated_at"])

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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 2)
        self.assertEqual(data["next"], None)
        self.assertEqual(data["previous"], None)
        result_data = data["results"][0]
        self.assertEqual(result_data["user"], self.business_user_2.id)
        self.assertEqual(result_data["title"], "Graphic Design Package")
        self.assertEqual(
            result_data["description"], self.offer_package_2.description
        )
        self.assertEqual(result_data["image"], self.offer_package_2.image)
        self.assertEqual(result_data["min_price"], 80)
        self.assertEqual(result_data["min_delivery_time"], 3)
        self.assertEqual(
            result_data["user_details"],
            {
                "first_name": "Sarah",
                "last_name": "Miller",
                "username": "sarah_miller",
            },
        )
        self.assertIsNotNone(result_data["created_at"])
        self.assertIsNotNone(result_data["updated_at"])

    def test_offer_list_filter_by_creator_id_1(self):
        self.client.force_authenticate(user=None)
        url = (
            reverse("offerpackage-list")
            + f"?creator_id={self.business_user_1.id}"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 1)

    def test_offer_list_filter_by_creator_id_2(self):
        self.client.force_authenticate(user=None)
        url = (
            reverse("offerpackage-list")
            + f"?creator_id={self.business_user_2.id}"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 1)

    def test_offer_list_filter_by_min_price(self):
        self.client.force_authenticate(user=None)
        url = reverse("offerpackage-list") + "?min_price=85"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 2)

    def test_offer_list_filter_by_search(self):
        self.client.force_authenticate(user=None)
        url = reverse("offerpackage-list") + "?search=Graphic"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 1)

    def test_offer_list_filter_by_max_delivery_time(self):
        self.client.force_authenticate(user=None)
        url = reverse("offerpackage-list") + "?max_delivery_time=5"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 2)

    def test_offer_list_order_by_min_price(self):
        self.client.force_authenticate(user=None)
        url = reverse("offerpackage-list") + "?ordering=min_price"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 2)
        self.assertEqual(data["results"][0]["id"], self.offer_package_2.id)
        self.assertEqual(data["results"][1]["id"], self.offer_package_1.id)

    def test_offer_list_order_by_updated_at(self):
        self.client.force_authenticate(user=None)
        url = reverse("offerpackage-list") + "?ordering=updated_at"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        print(json.dumps(data, indent=2))
        self.assertEqual(data["results"][0]["id"], 2)
        self.assertEqual(data["results"][1]["id"], 1)

    def test_offer_create_ok(self):
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
        data = response.json()
        self.assertEqual(data["title"], "Grafikdesign-Paket")
        self.assertEqual(
            data["description"],
            offer.get("description"),
        )
        self.assertEqual(len(data["details"]), 3)
        self.assertEqual(OfferPackage.objects.all().count(), 3)

    def test_offer_create_not_business_user(self):
        self.client = TestDataFactory.authenticate_user(self.customer_user_1)
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
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_offer_update_ok(self):
        url = reverse(
            "offerpackage-detail", kwargs={"pk": self.offer_package_1.pk}
        )
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["title"], patch_data.get("title"))
        self.assertEqual(len(data["details"]), 3)

    def test_offer_update_not_offer_owner(self):
        self.client = TestDataFactory.authenticate_user(self.business_user_2)
        url = reverse(
            "offerpackage-detail", kwargs={"pk": self.offer_package_1.pk}
        )
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
            price=10,
            offer_type="basic",
            features=["WebDev", "Anderes"],
            package=cls.offer_package,
        )

    def setUp(self):
        self.client = TestDataFactory.authenticate_user(self.user)

    def test_offer_detail_ok(self):
        url = reverse("offer-detail", kwargs={"pk": self.offer.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["id"], self.offer.id)
        self.assertEqual(data["title"], self.offer.title)
        self.assertEqual(
            data["delivery_time_in_days"], self.offer.delivery_time_in_days
        )
        self.assertEqual(data["offer_type"], self.offer.offer_type)
        self.assertEqual(data["price"], self.offer.price)
        self.assertEqual(data["features"], self.offer.features)
