from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UsernameExistsSerializer(serializers.Serializer):
    """Serializer for the UsernameExistsView"""

    username = serializers.CharField(required=True)
    exists = serializers.BooleanField(read_only=True)


class UserWhitelistSerializer(serializers.Serializer):
    """Serializer for the UserWhitelistView"""

    username = serializers.CharField(required=True)
    whitelist = serializers.BooleanField(default=True)


class LoginSerializer(TokenObtainPairSerializer):
    """Serializer for the LoginView"""

    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    access_expiration = serializers.DateTimeField(read_only=True)
    refresh_expiration = serializers.DateTimeField(read_only=True)
