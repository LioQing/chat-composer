from typing import Optional

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class IncorrectOldPasswordException(APIException):
    """Exception for old password is incorrect when changing password."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Old password is incorrect.")
    default_code = "incorrect_old_password"


class BadArgumentsException(APIException):
    """Exception for bad arguments."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Bad arguments.")
    default_code = "bad_arguments"

    def __init__(self, detail: Optional[str] = None):
        """Initialize the exception."""
        if detail is not None:
            self.detail = detail
        super().__init__(detail)
