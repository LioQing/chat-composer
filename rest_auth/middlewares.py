from typing import Callable

from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin

from core.models import ApiKey, User


class ApiKeyMiddleware(MiddlewareMixin):
    """Identify the user by the API key"""

    get_response: Callable[[HttpRequest], HttpResponse]

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def process_request(self, request: HttpRequest):
        """Identify the user by the API key"""
        if request.user.is_authenticated:
            return

        if request.headers.get("Authorization") is None:
            return

        if not request.headers.get("Authorization").startswith("Api-Key "):
            return

        api_key = request.headers.get("Authorization").replace("Api-Key ", "")
        try:
            user: User = ApiKey.objects.get_user_from_key(api_key)
        except ApiKey.DoesNotExist:
            return

        request.user = user
