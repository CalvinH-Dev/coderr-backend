from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from auth_app.api.permissions import IsProfileOwner
from auth_app.api.serializers import (
    BaseUserProfileBusinessSerializer,
    BaseUserProfileSerializer,
    LoginSerializer,
    RegistrationSerializer,
    UpdateUserProfileSerializer,
    UserProfileBusinessSerializer,
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
                "user_id": user.userprofile.pk,
            }
        )


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    API view for retrieving and updating user profiles.

    Allows authenticated users to GET or PATCH a user profile by ID.
    Returns 401 for unauthenticated requests.
    """

    serializer_class = UserProfileBusinessSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method == "PATCH":
            return [IsAuthenticated(), IsProfileOwner()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return UpdateUserProfileSerializer
        return super().get_serializer_class()


class BusinessProfilesView(generics.ListAPIView):
    """
    API view for listing business user profiles.

    Provides a read-only endpoint that returns a list of all business user
    profiles. Requires authentication to access.
    """

    serializer_class = BaseUserProfileBusinessSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(type="business")


class CustomerProfilesView(generics.ListAPIView):
    """
    API view for listing customer user profiles.

    Provides a read-only endpoint that returns a list of all customer user
    profiles. Requires authentication to access.
    """

    serializer_class = BaseUserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(type="customer")
