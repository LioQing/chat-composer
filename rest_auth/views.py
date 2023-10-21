from django.utils import timezone
from rest_framework import permissions
from rest_framework_simplejwt import views as jwt_views

from core.models import User


class ObtainTokenPairView(jwt_views.TokenObtainPairView):
    """Obtain access and refresh token pair"""

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """Return access and refresh token pair"""
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = User.objects.get(username=request.data["username"])
            user.last_login = timezone.now()
            user.save()
        return response


class TokenRefreshView(jwt_views.TokenRefreshView):
    """Refresh access token"""

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """Return access token"""
        return super().post(request, *args, **kwargs)
