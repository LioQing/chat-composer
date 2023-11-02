from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class UsernameDoesNotExist(APIException):
    """Exception for username not existing"""

    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _("Username does not exist")
    default_code = "username_does_not_exist"
