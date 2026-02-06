from rest_framework.authtoken.admin import User


class TestDataFactory:
    @staticmethod
    def create_authenticated_client(
        username="testuser",
        email="test@example.com",
        first_name="Max",
        last_name="Mustermann",
        password="testpass123",
        **kwargs,
    ):
        from rest_framework.test import APIClient

        client = APIClient()
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            **kwargs,
        )

        client.force_authenticate(user=user)
        return client, user
