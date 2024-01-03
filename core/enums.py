from utils.choice import BaseChoice


class ReturnType(BaseChoice):
    """Return type for components"""

    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    LIST = "list"
    DICTIONARY = "dictionary"
    NONE = "none"
