import json

from django.urls import reverse
from rest_framework import status

from core.test_factory.authenticate import TestDataFactory
from offers_app.tests import APITestCaseWithSetup

# Create your tests here.


class TestOrdersViewSet(APITestCaseWithSetup):
    def setUp(self):
        self.client = TestDataFactory.authenticate_user(self.customer_user_1)

    def test_create_order_ok(self):
        url = reverse("order-list")
        offer_package = self.offer_package_1
        offer = offer_package.offers.all().first()
        post_data = {"offer_detail_id": offer.id}
        response = self.client.post(url, post_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()

        self.assertEqual(data.pop("id"), 1)
        self.assertEqual(data.pop("customer_user"), self.customer_user_1.id)
        self.assertEqual(data.pop("business_user"), offer_package.user.id)
        self.assertEqual(data.pop("status"), "in_progress")
        self.assertEqual(data.pop("title"), offer.title)
        self.assertEqual(data.pop("revisions"), offer.revisions)
        self.assertEqual(
            data.pop("delivery_time_in_days"), offer.delivery_time_in_days
        )
        self.assertEqual(data.pop("price"), offer.price)
        self.assertEqual(data.pop("features"), offer.features)
        self.assertEqual(data.pop("offer_type"), offer.offer_type)
        self.assertIsNotNone(data.pop("created_at"))

        self.assertEqual(data, {}, f"Unexpected Fields: {data}")
