"""Enumerations for Vertex AI API."""

from enum import StrEnum, Enum


class GeminiRole(StrEnum):
    """Role of the content in Gemini API

    Attributes:
        USER: The user.
        MODEL: The model.
    """

    USER = "USER"
    MODEL = "MODEL"


class GeminiHarmCategory(Enum):
    """The category of a rating.

    Attributes:
        HARM_CATEGORY_UNSPECIFIED (0):
            Category is unspecified.
        HARM_CATEGORY_DEROGATORY (1):
            Negative or harmful comments targeting
            identity and/or protected attribute.
        HARM_CATEGORY_TOXICITY (2):
            Content that is rude, disrepspectful, or
            profane.
        HARM_CATEGORY_VIOLENCE (3):
            Describes scenarios depictng violence against
            an individual or group, or general descriptions
            of gore.
        HARM_CATEGORY_SEXUAL (4):
            Contains references to sexual acts or other
            lewd content.
        HARM_CATEGORY_MEDICAL (5):
            Promotes unchecked medical advice.
        HARM_CATEGORY_DANGEROUS (6):
            Dangerous content that promotes, facilitates,
            or encourages harmful acts.
        HARM_CATEGORY_HARASSMENT (7):
            Harasment content.
        HARM_CATEGORY_HATE_SPEECH (8):
            Hate speech and content.
        HARM_CATEGORY_SEXUALLY_EXPLICIT (9):
            Sexually explicit content.
        HARM_CATEGORY_DANGEROUS_CONTENT (10):
            Dangerous content.
    """

    HARM_CATEGORY_UNSPECIFIED = 0
    HARM_CATEGORY_DEROGATORY = 1
    HARM_CATEGORY_TOXICITY = 2
    HARM_CATEGORY_VIOLENCE = 3
    HARM_CATEGORY_SEXUAL = 4
    HARM_CATEGORY_MEDICAL = 5
    HARM_CATEGORY_DANGEROUS = 6
    HARM_CATEGORY_HARASSMENT = 7
    HARM_CATEGORY_HATE_SPEECH = 8
    HARM_CATEGORY_SEXUALLY_EXPLICIT = 9
    HARM_CATEGORY_DANGEROUS_CONTENT = 10


class GeminiHarmBlockThreshold(Enum):
    """Block at and beyond a specified harm probability.

    Attributes:
        HARM_BLOCK_THRESHOLD_UNSPECIFIED (0):
            Threshold is unspecified.
        BLOCK_LOW_AND_ABOVE (1):
            Content with NEGLIGIBLE will be allowed.
        BLOCK_MEDIUM_AND_ABOVE (2):
            Content with NEGLIGIBLE and LOW will be
            allowed.
        BLOCK_ONLY_HIGH (3):
            Content with NEGLIGIBLE, LOW, and MEDIUM will
            be allowed.
        BLOCK_NONE (4):
            All content will be allowed.
    """

    HARM_BLOCK_THRESHOLD_UNSPECIFIED = 0
    BLOCK_LOW_AND_ABOVE = 1
    BLOCK_MEDIUM_AND_ABOVE = 2
    BLOCK_ONLY_HIGH = 3
    BLOCK_NONE = 4
