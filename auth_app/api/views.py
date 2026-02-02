from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from auth_app.api.serializers import LoginSerializer, RegistrationSerializer


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
