from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import (
    TokenRefreshSerializer as jwtTokenRefreshSerializer,
)


class UsernameExistsSerializer(serializers.Serializer):
    """Serializer for the UsernameExistsView"""

    username = serializers.CharField(required=True)
    exists = serializers.BooleanField(read_only=True)


class IsWhitelistedSerializer(serializers.Serializer):
    """Serializer for the IsWhitelistedView"""

    is_whitelisted = serializers.BooleanField()


class UserWhitelistSerializer(serializers.Serializer):
    """Serializer for the UserWhitelistView"""

    username = serializers.CharField(required=True)
    whitelist = serializers.BooleanField(default=True)


class IsAdminSerializer(serializers.Serializer):
    """Serializer for the IsAdminView"""

    is_admin = serializers.BooleanField()


class LoginSerializer(TokenObtainPairSerializer):
    """Serializer for the LoginView"""

    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    access_expiration = serializers.DateTimeField(read_only=True)
    refresh_expiration = serializers.DateTimeField(read_only=True)


class TokenRefreshSerializer(jwtTokenRefreshSerializer):
    """Serializer for the TokenRefreshView"""

    access = serializers.CharField(read_only=True)
    access_expiration = serializers.DateTimeField(read_only=True)
