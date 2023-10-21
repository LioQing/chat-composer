from enum import StrEnum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, model_serializer


class Role(StrEnum):
    """Role enumeration for conversation messages"""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"

    def __repr__(self) -> str:
        """Get the string representation of the role"""
        return repr(self.value)


class FinishReason(StrEnum):
    """Finish reason enumeration for conversation messages"""

    STOP = "stop"
    LENGTH = "length"
    CONTENT_FILTER = "content_filter"
    FUNCTION_CALL = "function_call"

    def __repr__(self) -> str:
        """Get the string representation of the finish reason"""
        return repr(self.value)


class FunctionCall(BaseModel):
    """Function call"""

    arguments: str
    name: str


class Message(BaseModel):
    """Message for conversation"""

    content: str
    name: Optional[str] = Field(None)
    function_call: Optional[FunctionCall] = Field(None)
    role: Role

    @model_serializer
    def model_dump(self) -> Dict[str, Any]:
        """Dump the model"""
        dump = {"role": self.role, "content": self.content}

        if self.name is not None:
            dump["name"] = self.name

        if self.function_call is not None:
            dump["function_call"] = self.function_call

        return dump


class Choice(BaseModel):
    """Message choice by OpenAI API"""

    finish_reason: FinishReason
    index: int
    message: Message


class Usage(BaseModel):
    """Usage by OpenAI API"""

    completion_tokens: int
    prompt_tokens: int
    total_tokens: int


class Chatcmpl(BaseModel):
    """Chat completion by OpenAI API"""

    id: str
    choices: List[Choice]
    created: int
    model: str
    object: str
    usage: Usage


class FunctionCallRequest(BaseModel):
    """Function call for ChatCompletion.create"""

    auto: Optional[bool] = Field(False)
    name: Optional[str] = Field(None)

    @model_serializer
    def model_dump(self) -> Dict[str, Any] | str:
        """Dump the model"""
        if self.name is not None:
            return {"name": self.name}
        if self.auto:
            return "auto"

        return "none"


class Parameter(BaseModel):
    """Function parameter"""

    type: str
    description: str
    enum: Optional[List[str]] = Field(None)
    required: bool = Field(False, exclude=True)

    @model_serializer
    def model_dump(self) -> Dict[str, Any]:
        """Dump the model"""
        dump = {"type": self.type, "description": self.description}

        if self.enum is not None:
            dump["enum"] = self.enum

        return dump


class Parameters(BaseModel):
    """Parameters for function"""

    parameters: Dict[str, Parameter]

    @model_serializer
    def model_dump(self) -> Dict[str, Any]:
        """Dump the model"""
        dump = {
            "type": "object",
            "properties": {
                k: v.model_dump() for k, v in self.parameters.items()
            },
            "required": [
                k for k, v in self.parameters.items() if v.required is True
            ],
        }

        return dump


class Function(BaseModel):
    """Function"""

    description: str
    name: str
    parameters: Parameters


class ChatcmplRequest(BaseModel):
    """Chat completition request body"""

    deployment_id: str
    messages: List[Message]
    model: str
    frequency_penalty: float = Field(0.0, ge=-2.0, le=2.0)
    function_call: FunctionCallRequest = Field(
        default_factory=FunctionCallRequest
    )
    functions: Optional[List[Function]] = Field(None)
    max_tokens: int = Field(2048, gt=0)
    n: int = Field(1)
    presence_penalty: float = Field(0.0, ge=-2.0, le=2.0)
    stop: Optional[str | List[str]] = Field(None)
    stream: bool = Field(False)
    temperature: float = Field(1.0, ge=0.0, le=2.0)
    top_p: float = Field(1.0)
    user: Optional[str] = Field(None)

    def model_dump(self) -> Dict[str, Any]:
        """Dump the model"""
        dump = super().model_dump()

        if self.functions is None:
            dump.pop("functions")
            dump.pop("function_call")

        if self.stop is None:
            dump.pop("stop")

        if self.user is None:
            dump.pop("user")

        return dump
