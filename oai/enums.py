from utils.choice import BaseChoice


class Role(BaseChoice):
    """Role enumeration for conversation messages"""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"


class FinishReason(BaseChoice):
    """Finish reason enumeration for conversation messages"""

    STOP = "stop"
    LENGTH = "length"
    CONTENT_FILTER = "content_filter"
    FUNCTION_CALL = "function_call"
