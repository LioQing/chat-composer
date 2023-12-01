"""OpenAI API functions."""

from .models import Chatcmpl, ChatcmplRequest


def chatcmpl(request: ChatcmplRequest) -> Chatcmpl:
    """Call the OpenAI chat completion with the given request.

    The request and response are logged to the database.

    Args:
        request (models.ChatcmplRequest): The request to be sent to the API.

    Returns:
        models.Chatcmpl: The response from the API.
    """
    from engine.restricted.oai import (
        create_chatcmpl_models,
        logger,
        openai_chatcmpl,
    )

    request = request.model_dump()

    logger.debug(f"Calling OpenAI chat completion with request: {request}")

    response = openai_chatcmpl(**request)
    response = Chatcmpl(**response)

    logger.debug(f"API response: {response}")

    create_chatcmpl_models(request, response)

    return response
