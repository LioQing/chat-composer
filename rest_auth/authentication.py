from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication

from core.models import ApiKey


class ApiKeyAuthentication(TokenAuthentication):
    """Allow access only to users with API key."""

    keyword = "Api-Key"
    model = ApiKey

    def authenticate_credentials(self, key: str):
        """Check if API key is valid."""
        model = self.get_model()
        try:
            token = model.objects.get_from_key(key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_("Invalid token."))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(
                _("User inactive or deleted.")
            )

        return (token.user, token)
