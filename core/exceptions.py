from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class InvalidComponentCode(APIException):
    """Exception for when the adventure has already started."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Invalid component code.")
    default_code = "invalid_component_code"

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        self.detail = detail
