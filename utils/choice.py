from enum import StrEnum
from typing import List, Tuple


class BaseChoice(StrEnum):
    """Base choice class"""

    def __repr__(self) -> str:
        """Get the string representation of the role"""
        return repr(self.value)

    @classmethod
    def choices(cls) -> List[Tuple[str, str]]:
        """Get the choices for the choice"""
        return [(choice.value, choice.value) for choice in cls]
