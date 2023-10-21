import logging
from typing import List

import openai

from config.logger import logger_config
from config.openai import openai_config

from .models import (
    Chatcmpl,
    ChatcmplRequest,
    Function,
    FunctionCallRequest,
    Message,
)

openai.api_key = openai_config.key
openai.api_base = openai_config.url
openai.api_type = openai_config.api_type
openai.api_version = openai_config.version


logger = logging.getLogger(__name__)
logger.setLevel(logger_config.level)


def call_api_raw(request: ChatcmplRequest) -> Chatcmpl:
    """Call the OpenAI API with the given request"""
    request = request.model_dump()

    logger.debug(f"Calling API with request: {request}")

    response = openai.ChatCompletion.create(**request)
    response = Chatcmpl(**response)

    logger.debug(f"API response: {response}")

    return response


def call_api(messages: List[Message]) -> Chatcmpl:
    """Call the OpenAI API with the given messages"""
    request = ChatcmplRequest(
        deployment_id=openai_config.deployment,
        model=openai_config.model,
        messages=messages,
    )

    response = call_api_raw(request)

    if response.choices[0].message.content is None:
        logger.error("API response message is None")
        raise ValueError("API response message is None")

    return response


def call_api_function(messages: List[Message], function: Function) -> Chatcmpl:
    """Call the OpenAI API to provide arguments for the function"""
    request = ChatcmplRequest(
        deployment_id=openai_config.deployment,
        model=openai_config.model,
        messages=messages,
        functions=[function],
        function_call=FunctionCallRequest(name=function.name),
    )

    response = call_api_raw(request)

    if response.choices[0].message.function_call is None:
        logger.error("API Function is not called.")
        raise ValueError("API Function is not called.")

    return response
