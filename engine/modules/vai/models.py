"""Models for Vertex AI API.

This module only defines the request models in Pydantic. The response models
are defined in the Google API library `google.generativeai`, which is
imported to this module as `google_types`.

For more details, see the `google.generativeai` documentation:
https://ai.google.dev/docs.

And for more about the response type `GenerateContentResponse`, see:
https://ai.google.dev/api/python/google/generativeai/types/GenerateContentResponse.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from google.generativeai import types as google_types  # noqa: F401
from .enums import GeminiRole, GeminiHarmCategory, GeminiHarmBlockThreshold


class GeminiPart(BaseModel):
    """Gemini part.

    Attributes:
        text (str): The text.
    """

    text: str


class GeminiContent(BaseModel):
    """Gemini content.

    Attributes:
        parts (List[GeminiPart | str]): The parts.
        role (GeminiRole): The role.
    """

    parts: List[GeminiPart | str]
    role: GeminiRole


class GeminiGenerationConfig(BaseModel):
    """Gemini generation configuration.

    Attributes:
        candidate_count (int): The number of candidates to generate.
        stop_sequences (List[str]): The stop sequences.
        max_tokens (int): The maximum number of tokens to generate.
        temperature (float): The temperature.
        top_p (Optional[float]): The top p. Defaults to None.
        top_k (Optional[int]): The top k. Defaults to None.
    """

    candidate_count: int = Field(1, ge=1, le=1)
    stop_sequences: List[str] = Field([])
    max_tokens: int = Field(2048, ge=1, le=2048)
    temperature: float = Field(0.6, ge=0.0, le=1.0)
    top_p: Optional[float] = Field(None)
    top_k: Optional[int] = Field(None)

    def model_dump(self) -> Dict[str, Any]:
        """Dump the model to a dictionary."""
        return self.model_dump(exclude_none=True)


class GeminiSafetySetting(BaseModel):
    """Gemini safety setting.

    Attributes:
        harm_category (GeminiHarmCategory): The harm category.
        block_threshold (GeminiHarmBlockThreshold): The block threshold.
    """

    category: GeminiHarmCategory
    block_threshold: GeminiHarmBlockThreshold


class GeminiRequest(BaseModel):
    """Gemini request body.

    Attributes:
        contents (GeminiContent | GeminiPart | str): The content.
        generation_config (Optional[GeminiGenerationConfig]): The generation
            configuration. Defaults to None.
        safety_settings (Optional[GeminiSafetySetting]): The safety
            settings. Defaults to None.
    """

    contents: GeminiContent | GeminiPart | str
    generation_config: Optional[GeminiGenerationConfig] = Field(None)
    safety_settings: Optional[GeminiSafetySetting] = Field(None)
