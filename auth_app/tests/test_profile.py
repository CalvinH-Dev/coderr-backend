import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from auth_app.models import UserProfile
from core.test_factory.authenticate import TestDataFactory


class RetrieveProfileTest(APITestCase):
    def setUp(self) -> None:
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

        UserProfile.objects.create(user=self.user, **self.profile_data)

    def test_retrieve_profile_ok(self):
        url = reverse("profile-detail", None, kwargs={"id": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"], 1)  # type: ignore
        self.assertEqual(response.data["username"], "john_doe")  # type: ignore
        self.assertEqual(response.data["first_name"], "John")  # type: ignore
        self.assertEqual(response.data["last_name"], "Doe")  # type: ignore
        self.assertEqual(response.data["file"], "profile_picture.jpg")  # type: ignore
        self.assertEqual(response.data["location"], "Berlin")  # type: ignore
        self.assertEqual(response.data["tel"], "123456789")  # type: ignore
        self.assertEqual(response.data["description"], "Business description")  # type: ignore
        self.assertEqual(response.data["working_hours"], "9-17")  # type: ignore
        self.assertEqual(response.data["type"], "business")  # type: ignore
        self.assertEqual(response.data["email"], "john@example.com")  # type: ignore
        self.assertIsNotNone(response.data["created_at"])  # type: ignore

    def test_retrieve_profile_not_authenticated(self):
        self.client.force_authenticate(user=None)  # type: ignore
        url = reverse("profile-detail", None, kwargs={"id": 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_profile_not_found(self):
        url = reverse("profile-detail", None, kwargs={"id": 999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class RetrieveBusinessProfilesTest(APITestCase):
    def setUp(self) -> None:
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

        UserProfile.objects.create(user=self.user, **self.profile_data)

    def test_retrieve_business_profile_ok(self):
        url = reverse("profile-business-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        list = response.data  # type: ignore
        self.assertEqual(list[0]["user"], 1)
        self.assertEqual(list[0]["username"], "john_doe")
        self.assertEqual(list[0]["first_name"], "John")
        self.assertEqual(list[0]["last_name"], "Doe")
        self.assertEqual(list[0]["file"], "profile_picture.jpg")
        self.assertEqual(list[0]["location"], "Berlin")
        self.assertEqual(list[0]["tel"], "123456789")
        self.assertEqual(list[0]["description"], "Business description")
        self.assertEqual(list[0]["working_hours"], "9-17")
        self.assertEqual(list[0]["type"], "business")


class RetrieveCustomerProfilesTest(APITestCase):
    def setUp(self) -> None:
        self.client, self.user = TestDataFactory.create_authenticated_client(
            username="john_doe",
            email="john@example.com",
            first_name="John",
            last_name="Doe",
        )
        self.profile_data = {
            "file": "profile_picture.jpg",
            "type": "customer",
        }

        UserProfile.objects.create(user=self.user, **self.profile_data)

    def test_retrieve_business_profile_ok(self):
        url = reverse("profile-customer-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        list = response.data  # type: ignore
        self.assertEqual(list[0]["user"], 1)
        self.assertEqual(list[0]["username"], "john_doe")
        self.assertEqual(list[0]["first_name"], "John")
        self.assertEqual(list[0]["last_name"], "Doe")
        self.assertEqual(list[0]["file"], "profile_picture.jpg")
        self.assertEqual(list[0]["type"], "customer")
