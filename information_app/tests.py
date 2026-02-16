from django.urls import reverse
from rest_framework import status

from core.test_factory.data import APITestCaseWithSetup
from information_app.api.helpers import (
    get_average_rating,
    get_business_profile_count,
    get_offer_count,
    get_review_count,
)


class TestOfferPackageViewSet(APITestCaseWithSetup):
    def test_base_info_ok(self):
        expected_data = {
            "review_count": get_review_count(),
            "average_rating": get_average_rating(),
            "business_profile_count": get_business_profile_count(),
            "offer_count": get_offer_count(),
        }
        url = reverse("base-info")
        response = self.client.get(url)

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            data.pop("review_count"), expected_data["review_count"]
        )
        self.assertEqual(
            data.pop("average_rating"), expected_data["average_rating"]
        )
        self.assertEqual(
            data.pop("business_profile_count"),
            expected_data["business_profile_count"],
        )
        self.assertEqual(data.pop("offer_count"), expected_data["offer_count"])

        self.assertEqual(data, {})

    def test_base_info_not_authorized(self):
        self.client.force_authenticate(user=None)
        url = reverse("base-info")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
