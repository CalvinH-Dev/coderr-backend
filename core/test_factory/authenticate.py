"""
Test data factory for Django REST Framework tests.

This module provides utility classes for creating test data and authenticated
clients in Django REST Framework test cases.
"""

from rest_framework.authtoken.admin import User


class TestDataFactory:
    """
    Factory class for creating test data and authenticated API clients.

    This class provides static methods to simplify the creation of authenticated
    users and API clients for testing Django REST Framework applications.
    """

    @staticmethod
    def create_authenticated_client(
        username="testuser",
        email="test@example.com",
        first_name="Max",
        last_name="Mustermann",
        password="testpass123",
        **kwargs,
    ):
        """
        Create an authenticated API client with a new user.

        Creates a new user in the database and returns an authenticated API client
        that can be used in tests without requiring login credentials.

        Args:
            username (str, optional): Username for the new user.
                Defaults to "testuser".
            email (str, optional): Email address for the new user.
                Defaults to "test@example.com".
            first_name (str, optional): First name of the user.
                Defaults to "Max".
            last_name (str, optional): Last name of the user.
                Defaults to "Mustermann".
            password (str, optional): Password for the user account.
                Defaults to "testpass123".
            **kwargs: Additional keyword arguments passed to
            User.objects.create_user().
                Can include fields like 'is_staff', 'is_superuser', etc.

        Returns:
            tuple: A tuple containing:
                - client (APIClient): Authenticated API client instance.
                - user (User): Created user instance.
        """
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

    @staticmethod
    def authenticate_user(user):
        """
        Create an authenticated API client for an existing user.

        Takes an existing user instance and returns an API client authenticated
        as that user. The user reference is also stored on the client for
        convenient access during tests.

        Args:
            user (User): Existing user instance to authenticate with.

        Returns:
            APIClient: Authenticated API client instance with the user
                authenticated and stored in the 'authenticated_user' attribute.
        """
        from rest_framework.test import APIClient

        client = APIClient()
        client.force_authenticate(user=user)
        client.authenticated_user = user
        return client
