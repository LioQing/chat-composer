"""Vertex AI module."""

from . import models, api  # noqa: F401

# containment: not contained

import logging

from config.vertexai import vertexai_config
import google.generativeai as genai
from google.generativeai.types import GenerateContentResponse

genai.configure(api_key=vertexai_config.api_key)
model = genai.GenerativeModel("gemini-pro")


logger = logging.getLogger(__name__)


def gemini_pro(
    contents: models.google_types.ContentsType,
    generation_config: models.google_types.GenerationConfigType | None = None,
    safety_settings: models.google_types.SafetySettingDict | None = None,
    stream: bool = False,
) -> GenerateContentResponse:
    """Call the Vertex AI Gemini chat with the given request.

    The request and response are logged to the database.

    Args:
        contents (ContentsType): The contents to be sent to the API.
        generation_config (Optional[GenerationConfig]): The generation
            configuration. Defaults to None.
        safety_settings (Optional[SafetySettingDict]): The safety
            settings. Defaults to None.
        stream (bool): Whether to stream the response. Defaults to False.

    Returns:
        GenerateContentResponse: The response from the API.
    """
    # Create the client
    response = model.generate_content(
        contents,
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=stream,
    )

    return response


# containment: end
