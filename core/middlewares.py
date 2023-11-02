import logging
from typing import Callable

from django.http import HttpRequest, HttpResponse

from config.logger import logger_config


class RequestLogMiddleware:
    """Log the request"""

    logger: logging.Logger
    get_response: Callable[[HttpRequest], HttpResponse]

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logger_config.level)

    def __call__(self, request: HttpRequest):
        """Log the request and response"""
        log_data = {
            "user": request.user.pk,
            "remote_address": request.META["REMOTE_ADDR"],
            "request_method": request.method,
            "request_path": request.get_full_path(),
            "request_headers": request.headers,
            "request_body": request.body,
        }

        response: HttpResponse = self.get_response(request)
        if request.method != "DELETE":
            if (
                response.has_header("content-type")
                and response["content-type"] == "application/json"
            ):
                if getattr(response, "streaming", False):
                    response_body = "<<<Streaming>>>"
                else:
                    response_body = response.content
            else:
                response_body = "<<<Not JSON>>>"

            log_data = log_data | {
                "response_status": response.status_code,
                "response_body": response_body,
            }

        self.logger.debug("%s", log_data)

        return response
