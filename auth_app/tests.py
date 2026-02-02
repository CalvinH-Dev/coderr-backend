from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from auth_app.models import UserProfile


class RegistrationTest(APITestCase):
    def setUp(self):
        self.data = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "customer",
        }

    def test_registration(self):
        url = reverse("registration")
        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "exampleUsername")
        self.assertEqual(UserProfile.objects.get().user_id, 1)  # type: ignore
        self.assertEqual(UserProfile.objects.get().type, "customer")


class LoginTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="exampleUsername",
            email="example@mail.de",
            password="examplePassword",
        )
        UserProfile.objects.create(user=self.user, type="customer")
        token_obj = Token.objects.create(user=self.user)
        self.token = token_obj.key

    def test_login(self):
        url = reverse("login")
        data = {
            "username": "exampleUsername",
            "password": "examplePassword",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["token"], self.token)  # type: ignore
        self.assertEqual(response.data["username"], "exampleUsername")  # type: ignore
