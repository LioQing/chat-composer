from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework_api_key.permissions import BaseHasAPIKey

from core.models import ApiKey, User


class HasApiKey(BaseHasAPIKey):
    """Allow access only to users with API key."""

    model = ApiKey


class IsWhitelisted(BasePermission):
    """Allow access only to whitelisted users."""

    message = "You are not whitelisted."

    def has_permission(self, request: Request, view) -> bool:
        """Check if user is whitelisted."""
        user: User = request.user
        return user.is_authenticated and user.is_whitelisted
