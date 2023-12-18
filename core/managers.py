import base64
from typing import TYPE_CHECKING

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from django.conf import settings
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db import models
from rest_framework_api_key.models import BaseAPIKeyManager

if TYPE_CHECKING:
    from core.models import User


class UserManager(DjangoUserManager):
    """Manager for the user"""

    def get_with_api_key(self, api_key: str):
        """Get the user with the given API key"""
        return self.get(api_key=api_key)


class ApiKeyManager(BaseAPIKeyManager):
    """Manager for the API key"""

    def get_user_from_key(self, key: str) -> "User":
        """Get the user from the given API key"""
        api_key = self.get_from_key(key)
        return api_key.user

    def get_key_from_user(self, user: "User", password: str) -> str:
        """Get the decrypted key from the given user"""
        api_key = user.api_key
        key: str = self.decrypt_api_key(self, password, api_key.encrypted_key)
        return key

    def create_key(self, user: "User", password: str) -> str:
        """Create an API key"""
        from core.models import ApiKey

        # Destroy existing key
        try:
            user.api_key.delete()
        except ApiKey.DoesNotExist:
            pass

        # Create key
        obj, key = super().create_key(
            name=user.username[:50],
            user=user,
        )
        obj.encrypted_key = self.encrypt_api_key(self, password, key)
        obj.save()
        return key

    @staticmethod
    def encrypt_api_key(self, password: str, api_key: str) -> str:
        """Encrypt the API key"""
        salt = settings.SECRET_KEY.encode()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        f = Fernet(key)
        return f.encrypt(api_key.encode()).decode()

    @staticmethod
    def decrypt_api_key(self, password: str, api_key: str) -> str:
        """Decrypt the API key"""
        salt = settings.SECRET_KEY.encode()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        f = Fernet(key)
        return f.decrypt(api_key.encode()).decode()


class ActivePipelineManager(models.Manager):
    """Manager for the active pipelines"""

    def get_queryset(self):
        """Return the active pipelines"""
        return super().get_queryset().filter(is_active=True)


class ActiveComponentInstanceManager(models.Manager):
    """Manager for the active component instnaces"""

    def get_queryset(self):
        """Return the active component instnaces"""
        return super().get_queryset().filter(is_active=True)
