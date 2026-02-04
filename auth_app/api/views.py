from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from auth_app.api.permissions import IsAuthenticatedOr401
from auth_app.api.serializers import (
    LoginSerializer,
    RegistrationSerializer,
    UserProfileSerializer,
)
from auth_app.models import UserProfile


class RegistrationView(generics.CreateAPIView):
    """
    API view for registering a new user.

    Uses the RegistrationSerializer to handle incoming POST requests
    with registration details and create a new user and profile.
    """

    permission_classes = []
    serializer_class = RegistrationSerializer


class LoginView(ObtainAuthToken):
    """
    API view to authenticate a user and return a token.

    Accepts login credentials via POST, validates them using the
    LoginSerializer, and returns an auth token along with user info.
    """

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for user login.

        Validates the request data, retrieves the authenticated user,
        and returns a Response containing the token and basic user information.
        """
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]  # type: ignore
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.pk,
            }
        )


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    API view for retrieving and updating user profiles.

    Allows authenticated users to GET or PATCH a user profile by ID.
    Returns 401 for unauthenticated requests instead of the default 403.
    """

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticatedOr401]
    queryset = UserProfile.objects.all()
    http_method_names = ["get", "patch", "head", "options"]
    lookup_field = "id"
