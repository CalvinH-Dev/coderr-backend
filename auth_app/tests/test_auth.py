from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from auth_app.models import UserProfile


class RegistrationTest(APITestCase):
    def setUp(self):
        self.user_data = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "customer",
        }

    def test_registration_ok(self):
        url = reverse("registration")
        response = self.client.post(url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(
            User.objects.get().username, self.user_data["username"]
        )
        self.assertEqual(UserProfile.objects.get().user_id, 1)  # type: ignore
        self.assertEqual(
            UserProfile.objects.get().type, self.user_data["type"]
        )

    def test_registration_password_mismatch(self):
        url = reverse("registration")
        user_data = self.user_data.copy()
        user_data["repeated_password"] = "differentPassword"

        response = self.client.post(url, user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(UserProfile.objects.count(), 0)

    def test_registration_missing_username(self):
        url = reverse("registration")
        user_data = self.user_data.copy()
        del user_data["username"]

        response = self.client.post(url, user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(UserProfile.objects.count(), 0)

    def test_registration_missing_email(self):
        url = reverse("registration")
        user_data = self.user_data.copy()
        del user_data["email"]

        response = self.client.post(url, user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(UserProfile.objects.count(), 0)

    def test_registration_duplicate_username(self):
        url = reverse("registration")
        self.client.post(url, self.user_data, format="json")

        response = self.client.post(url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(UserProfile.objects.count(), 1)

    def test_registration_invalid_email(self):
        url = reverse("registration")
        user_data = self.user_data.copy()
        user_data["email"] = "invalid-email"

        response = self.client.post(url, user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(UserProfile.objects.count(), 0)


class LoginTest(APITestCase):
    def setUp(self):
        self.user_data = {
            "username": "exampleUsername",
            "password": "examplePassword",
        }
        self.user = User.objects.create_user(
            email="example@mail.de",
            **self.user_data,
        )
        UserProfile.objects.create(user=self.user, type="customer")
        token_obj = Token.objects.create(user=self.user)
        self.token = token_obj.key

    def test_login_ok(self):
        url = reverse("login")
        response = self.client.post(url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["token"], self.token)
        self.assertEqual(data["username"], "exampleUsername")

    def test_login_wrong_password(self):
        url = reverse("login")
        user_data = self.user_data.copy()
        user_data["password"] = "wrongPassword"

        response = self.client.post(url, user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_wrong_username(self):
        url = reverse("login")
        user_data = self.user_data.copy()
        user_data["username"] = "wrongUsername"

        response = self.client.post(url, user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_missing_username(self):
        url = reverse("login")
        user_data = self.user_data.copy()
        del user_data["username"]

        response = self.client.post(url, user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_missing_password(self):
        url = reverse("login")
        user_data = self.user_data.copy()
        del user_data["password"]

        response = self.client.post(url, user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_empty_credentials(self):
        url = reverse("login")
        user_data = self.user_data.copy()
        user_data["username"] = ""
        user_data["password"] = ""

        response = self.client.post(url, user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_nonexistent_user(self):
        url = reverse("login")
        user_data = self.user_data.copy()
        user_data["username"] = "nonexistentuser"
        user_data["password"] = "somepassword"

        response = self.client.post(url, user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
