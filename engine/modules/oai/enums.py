"""Enumerations for OpenAI API."""

from enum import StrEnum


class Role(StrEnum):
    """Role enumeration for conversation messages.

    Attributes:
        SYSTEM: system.
        USER: user.
        ASSISTANT: assistant.
        FUNCTION: function.
    """

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"

    def __repr__(self) -> str:
        """Get the string representation of the role"""
        return repr(self.value)


class FinishReason(StrEnum):
    """Finish reason enumeration for conversation messages.

    Attributes:
        STOP: stop.
        LENGTH: length.
        CONTENT_FILTER: content_filter.
        FUNCTION_CALL: function_call.
    """

    STOP = "stop"
    LENGTH = "length"
    CONTENT_FILTER = "content_filter"
    FUNCTION_CALL = "function_call"

    def __repr__(self) -> str:
        """Get the string representation of the finish reason"""
        return repr(self.value)
