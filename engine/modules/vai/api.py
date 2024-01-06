"""Vertex AI API functions."""

# containment: contained
# import requests

# containment: end

from .models import (
    GeminiRequest,
    google_types,
)


def gemini_pro(request: GeminiRequest) -> google_types.GenerateContentResponse:
    """Call the Gemini Pro chat with the given request.

    Args:
        request (GeminiRequest): The request.

    Returns:
        GenerateContentResponse: The response from the API.
    """
    # containment: not contained
    from engine.modules.vai import (
        gemini_pro,
        create_gemini_pro_models,
        logger,
    )

    request = request.model_dump()

    logger.debug(f"Calling Gemini Pro with request: {request}")

    response = gemini_pro(**request)

    logger.debug(f"API response: {response}")

    create_gemini_pro_models(request, response)

    return response
    # containment: else
    # from modules import composer
    # from google.ai.generativelanguage_v1beta.types import (
    #     GenerateContentResponse,
    # )

    # response = requests.post(
    #     composer.url(
    #         f"conductor/chat/vai/gemini-pro/{composer.component_id()}/"
    #     ),
    #     json={"request": request.model_dump()},
    #     headers=composer.headers(),
    # )
    # response.raise_for_status()
    # response = response.json()["response"]
    # response = google_types.GenerateContentResponse.from_response(
    #     GenerateContentResponse(response)
    # )

    # return response
    # containment: end
