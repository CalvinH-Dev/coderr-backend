from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from auth_app.api.authenticate_user import authenticate_user
from auth_app.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.

    Provides a read-only representation of basic user information
    including id, username, name, and email.
    """

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username"]


class BaseUserProfileSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            "file",
            "type",
        ]

    def get_file(self, obj):
        if obj.file:
            return obj.file.name
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["user"] = instance.user.id
        data["username"] = instance.user.username
        data["first_name"] = instance.user.first_name
        data["last_name"] = instance.user.last_name
        return data


class BaseUserProfileBusinessSerializer(BaseUserProfileSerializer):
    file = serializers.SerializerMethodField()

    class Meta(BaseUserProfileSerializer.Meta):
        model = UserProfile
        fields = BaseUserProfileSerializer.Meta.fields + [
            "location",
            "tel",
            "description",
            "working_hours",
        ]


class UserProfileCustomerSerializer(BaseUserProfileSerializer):
    class Meta(BaseUserProfileSerializer.Meta):
        fields = BaseUserProfileSerializer.Meta.fields + ["created_at"]
        read_only_fields = ["created_at"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["email"] = instance.user.email
        return data


class UserProfileBusinessSerializer(BaseUserProfileBusinessSerializer):
    """
    Serializer for the UserProfile model.

    Serializes user profile data and automatically includes related
    User fields (user id, username, email, first_name, last_name) in
    the output representation. The file field is converted to show
    only the filename instead of the full path.
    """

    class Meta(BaseUserProfileBusinessSerializer.Meta):
        fields = BaseUserProfileBusinessSerializer.Meta.fields + ["created_at"]
        read_only_fields = ["created_at"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["email"] = instance.user.email
        return data


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.

    Handles incoming registration data, enforces email and username
    uniqueness, matches password fields, and creates the User
    along with a related UserProfile. Returns a token and
    profile information on output.
    """

    repeated_password = serializers.CharField(max_length=100, write_only=True)
    type = serializers.ChoiceField(
        choices=UserProfile.Type.choices, write_only=True
    )
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Email already exists",
            )
        ],
    )
    username = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Username already exists",
            )
        ],
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "repeated_password", "type"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError(
                {"error": "Password and repeated password don't match"}
            )
        return attrs

    def create(self, validated_data):
        profile_type = validated_data.pop("type")
        validated_data.pop("repeated_password")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        UserProfile.objects.create(user=user, type=profile_type)

        return user

    def to_representation(self, instance):
        token, created = Token.objects.get_or_create(user=instance)
        return {
            "token": token.key,
            "username": instance.username,
            "email": instance.email,
            "user_id": instance.id,
        }


class LoginSerializer(serializers.Serializer):
    """
    Serializer for handling user login input and validation.

    Defines the expected fields for login, including username and
    password. Validates credentials using the authenticate_user function.
    """

    username = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate_user(attrs)
        attrs["user"] = user

        return attrs
