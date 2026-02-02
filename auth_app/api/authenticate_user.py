from rest_framework import serializers
from rest_framework.authentication import authenticate

from auth_app.api.dicts import LoginUserDict


def authenticate_user(attrs: LoginUserDict):
    """
    Authenticate a user based on provided login credentials.

    Given a dictionary with email and password, attempts to
    authenticate the user using Django's authentication system.
    Raises a validation error when credentials are invalid,
    otherwise returns the authenticated User instance.
    """
    username = attrs.get("username")
    password = attrs.get("password")

    user = authenticate(username=username, password=password)
    if not user:
        raise serializers.ValidationError(
            f"Invalid username or password for {username} and {password}"
        )
    return user
