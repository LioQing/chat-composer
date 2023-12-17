from typing import Dict, List, TypeAlias

JsonType: TypeAlias = (
    str | int | float | bool | None | List["JsonType"] | Dict[str, "JsonType"]
)
