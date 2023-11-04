import logging
from datetime import timedelta

from django.utils import timezone
from rest_framework import generics, permissions, response, views
from rest_framework_simplejwt import views as jwt_views

from core.models import User

from . import serializers


class UsernameExistsView(generics.CreateAPIView, views.APIView):
    """Check if username exists"""

    serializer_class = serializers.UsernameExistsSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request: views.Request):
        """Return whether username exists"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        exists = User.objects.filter(username=username).exists()
        serializer.validated_data["exists"] = exists
        return views.Response(serializer.validated_data)


class UserWhitelistView(generics.CreateAPIView, views.APIView):
    """View for whitelisting a user"""

    serializer_class = serializers.UserWhitelistSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        """Whitelist the user"""
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            username: str = serializer.validated_data["username"]
            whitelist: bool = serializer.validated_data["whitelist"]

            user = User.objects.get(username=username)
            user.is_whitelisted = whitelist
            user.save()
            return response.Response(serializer.data)
        except Exception as e:
            import traceback

            traceback.print_exc()
            logger = logging.getLogger(__name__)
            logger.error(e)
            raise e


class LoginView(jwt_views.TokenObtainPairView):
    """Obtain access and refresh token pair"""

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """Return access and refresh token pair"""
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = User.objects.get(username=request.data["username"])
            user.last_login = timezone.now()
            user.save()
            response.data["access_expiration"] = timezone.now() + timedelta(
                days=1
            )
            response.data["refresh_expiration"] = timezone.now() + timedelta(
                days=90
            )
        return response


class TokenRefreshView(jwt_views.TokenRefreshView):
    """Refresh access token"""

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """Return access token"""
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            response.data["access_expiration"] = timezone.now() + timedelta(
                days=1
            )
        return response
