from enum import StrEnum
from typing import List, Tuple


class Role(StrEnum):
    """Role enumeration for conversation messages"""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"

    def __repr__(self) -> str:
        """Get the string representation of the role"""
        return repr(self.value)

    @classmethod
    def choices(cls) -> List[Tuple[str, str]]:
        """Get the choices for the role"""
        return [(role.value, role.value) for role in cls]


class FinishReason(StrEnum):
    """Finish reason enumeration for conversation messages"""

    STOP = "stop"
    LENGTH = "length"
    CONTENT_FILTER = "content_filter"
    FUNCTION_CALL = "function_call"

    def __repr__(self) -> str:
        """Get the string representation of the finish reason"""
        return repr(self.value)

    @classmethod
    def choices(cls) -> List[Tuple[str, str]]:
        """Get the choices for the finish reason"""
        return [
            (finish_reason.value, finish_reason.value) for finish_reason in cls
        ]
