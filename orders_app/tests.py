import json

from django.urls import reverse
from rest_framework import status

from core.test_factory.authenticate import TestDataFactory
from offers_app.tests import APITestCaseWithSetup
from orders_app.models import Order

# Create your tests here.


class TestOrdersViewSet(APITestCaseWithSetup):
    def setUp(self):
        self.client = TestDataFactory.authenticate_user(self.customer_user_1)

    def test_order_list_ok(self):
        url = reverse("order-list")
        response = self.client.get(url)

        data = response.json()[0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.pop("id"), self.order_1.id)
        self.assertEqual(data.pop("business_user"), self.business_user_1.id)
        self.assertEqual(data.pop("customer_user"), self.customer_user_1.id)
        self.assertEqual(data.pop("title"), self.standard_web_offer.title)
        self.assertEqual(
            data.pop("revisions"), self.standard_web_offer.revisions
        )
        self.assertEqual(
            data.pop("delivery_time_in_days"),
            self.standard_web_offer.delivery_time_in_days,
        )
        self.assertEqual(
            data.pop("offer_type"), self.standard_web_offer.offer_type
        )
        self.assertEqual(data.pop("price"), self.standard_web_offer.price)
        self.assertEqual(
            data.pop("features"), self.standard_web_offer.features
        )
        self.assertEqual(data.pop("status"), "in_progress")
        self.assertIsNotNone(data.pop("created_at"))

        self.assertEqual(data, {}, f"Unexpected Fields: {data}")

    def test_order_list_not_authorized(self):
        self.client.force_authenticate(user=None)
        url = reverse("order-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_create_ok(self):
        url = reverse("order-list")
        last_id_before_post = Order.objects.order_by("-id").first().id
        offer = self.basic_design_offer
        post_data = {"offer_detail_id": offer.id}
        response = self.client.post(url, post_data, format="json")

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data.pop("id"), last_id_before_post + 1)
        self.assertEqual(data.pop("customer_user"), self.customer_user_1.id)
        self.assertEqual(data.pop("business_user"), offer.package.user.id)
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

    def test_order_create_forbidden(self):
        self.client = TestDataFactory.authenticate_user(self.business_user_1)
        url = reverse("order-list")
        post_data = {"offer_detail_id": 1}
        response = self.client.post(url, post_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_order_create_not_authorized(self):
        self.client.force_authenticate(user=None)
        url = reverse("order-list")
        post_data = {"offer_detail_id": 1}
        response = self.client.post(url, post_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_patch_ok(self):
        self.client = TestDataFactory.authenticate_user(self.business_user_1)

        order = self.order_1
        new_status = "completed"
        url = reverse("order-detail", kwargs={"pk": order.id})
        post_data = {"status": new_status}
        response = self.client.patch(url, post_data, format="json")

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.pop("id"), order.id)
        self.assertEqual(data.pop("customer_user"), order.customer_user.id)
        self.assertEqual(data.pop("business_user"), order.business_user.id)
        self.assertEqual(data.pop("status"), new_status)
        self.assertEqual(data.pop("title"), order.title)
        self.assertEqual(data.pop("revisions"), order.revisions)
        self.assertEqual(
            data.pop("delivery_time_in_days"), order.delivery_time_in_days
        )
        self.assertEqual(data.pop("price"), order.price)
        self.assertEqual(data.pop("features"), order.features)
        self.assertEqual(data.pop("offer_type"), order.offer_type)
        self.assertIsNotNone(data.pop("created_at"))

        self.assertEqual(data, {}, f"Unexpected Fields: {data}")

    def test_order_patch_forbidden(self):
        order = self.order_1
        new_status = "completed"
        url = reverse("order-detail", kwargs={"pk": order.id})
        post_data = {"status": new_status}
        response = self.client.patch(url, post_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_order_patch_not_authorized(self):
        self.client.force_authenticate(user=None)
        order = self.order_1
        new_status = "completed"
        url = reverse("order-detail", kwargs={"pk": order.id})
        post_data = {"status": new_status}
        response = self.client.patch(url, post_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
