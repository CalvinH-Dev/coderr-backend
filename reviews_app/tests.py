import json

from django.urls import reverse
from rest_framework import status

from core.test_factory.authenticate import TestDataFactory
from core.test_factory.data import APITestCaseWithSetup
from reviews_app.models import Review

# Create your tests here.


class TestReviewViewSet(APITestCaseWithSetup):
    def setUp(self):
        self.client = TestDataFactory.authenticate_user(self.customer_user_1)

    def test_reviews_list_ok(self):
        url = reverse("review-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        reviews = Review.objects.all()
        review_count = reviews.count()
        first_review_db = reviews.filter(id=1).first()

        data = response.json()
        self.assertEqual(len(data), review_count)
        first_review = data[0]

        self.assertEqual(first_review.pop("id"), first_review_db.id)
        self.assertEqual(
            first_review.pop("business_user"), first_review_db.business_user.id
        )
        self.assertEqual(
            first_review.pop("reviewer"), first_review_db.reviewer.id
        )
        self.assertEqual(first_review.pop("rating"), first_review_db.rating)
        self.assertEqual(
            first_review.pop("description"), first_review_db.description
        )
        self.assertIsNotNone(first_review.pop("created_at"))
        self.assertIsNotNone(first_review.pop("updated_at"))

        self.assertEqual(
            first_review, {}, "Response contains unexpected fields"
        )

    def test_reviews_list_not_authorized(self):
        self.client.force_authenticate(user=None)
        url = reverse("review-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_create_ok(self):
        self.client = TestDataFactory.authenticate_user(self.customer_user_2)
        url = reverse("review-list")
        last_review_id_before = Review.objects.all().order_by("id").last().id
        review = {
            "business_user": 2,
            "rating": 4,
            "description": "Alles war toll!",
        }
        response = self.client.post(url, review, format="json")

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(data.pop("id"), last_review_id_before + 1)
        self.assertEqual(data.pop("business_user"), review["business_user"])
        self.assertEqual(
            data.pop("reviewer"), self.client.authenticated_user.id
        )
        self.assertEqual(data.pop("rating"), review["rating"])
        self.assertEqual(data.pop("description"), review["description"])
        self.assertIsNotNone(data.pop("created_at"))
        self.assertIsNotNone(data.pop("updated_at"))

        self.assertEqual(data, {})

    def test_review_create_bad_request(self):
        authenticated_user = self.client.authenticated_user
        reviews_by_user = authenticated_user.written_reviews.all()
        existing_review = reviews_by_user.first()
        url = reverse("review-list")

        review_data = {
            "business_user": existing_review.business_user.id,
            "rating": existing_review.rating,
            "description": existing_review.description,
        }

        response = self.client.post(url, review_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_create_not_authorized(self):
        self.client.force_authenticate(user=None)

        url = reverse("review-list")
        review = {
            "business_user": 2,
            "rating": 4,
            "description": "Alles war toll!",
        }
        response = self.client.post(url, review, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_create_forbidden(self):
        self.client = TestDataFactory.authenticate_user(self.business_user_1)
        url = reverse("review-list")
        review = {
            "business_user": 2,
            "rating": 4,
            "description": "Alles war toll!",
        }
        response = self.client.post(url, review, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_review_update_ok(self):
        user = self.client.authenticated_user
        id_business_user = 1
        review_id_before = (
            user.written_reviews.filter(business_user=id_business_user)
            .first()
            .id
        )
        review = {"rating": 5, "description": "Noch besser als erwartet!"}
        url = reverse("review-detail", kwargs={"pk": review_id_before})
        response = self.client.patch(url, review, format="json")

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data.pop("id"), review_id_before)
        self.assertEqual(data.pop("business_user"), id_business_user)
        self.assertEqual(
            data.pop("reviewer"), self.client.authenticated_user.id
        )
        self.assertEqual(data.pop("rating"), review["rating"])
        self.assertEqual(data.pop("description"), review["description"])
        self.assertIsNotNone(data.pop("created_at"))
        self.assertIsNotNone(data.pop("updated_at"))

        self.assertEqual(data, {})

    def test_review_update_bad_request(self):
        user = self.client.authenticated_user
        review_id_before = (
            user.written_reviews.filter(business_user=1).first().id
        )
        review = {
            "rating": 6,
        }
        url = reverse("review-detail", kwargs={"pk": review_id_before})
        response = self.client.patch(url, review, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_update_not_authorized(self):
        self.client.force_authenticate(user=None)
        user = self.client.authenticated_user
        review_id_before = (
            user.written_reviews.filter(business_user=1).first().id
        )
        review = {
            "rating": 5,
        }
        url = reverse("review-detail", kwargs={"pk": review_id_before})
        response = self.client.patch(url, review, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_update_forbidden(self):
        user = self.customer_user_2
        review_id_before = (
            user.written_reviews.filter(business_user=1).first().id
        )
        review = {
            "rating": 5,
        }
        url = reverse("review-detail", kwargs={"pk": review_id_before})
        response = self.client.patch(url, review, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_review_update_not_found(self):
        review = {
            "rating": 5,
        }
        url = reverse("review-detail", kwargs={"pk": 999})
        response = self.client.patch(url, review, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_review_delete_ok(self):
        user = self.client.authenticated_user
        id_business_user = 1
        review_id_before = (
            user.written_reviews.filter(business_user=id_business_user)
            .first()
            .id
        )

        url = reverse("review-detail", kwargs={"pk": review_id_before})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_review_delete_not_authorized(self):
        self.client.force_authenticate(user=None)
        user = self.client.authenticated_user
        id_business_user = 1
        review_id_before = (
            user.written_reviews.filter(business_user=id_business_user)
            .first()
            .id
        )

        url = reverse("review-detail", kwargs={"pk": review_id_before})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_delete_forbidden(self):
        user = self.customer_user_2
        id_business_user = 1
        review_id_before = (
            user.written_reviews.filter(business_user=id_business_user)
            .first()
            .id
        )

        url = reverse("review-detail", kwargs={"pk": review_id_before})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_review_delete_not_found(self):
        url = reverse("review-detail", kwargs={"pk": 999})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
