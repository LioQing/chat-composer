"""Models for OpenAI API."""

# isort:skip_file

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, model_serializer

# containment: not contained
from config.openai import openai_config
# containment: end

from .enums import FinishReason, Role


class FunctionCall(BaseModel):
    """Function call by chat completion.

    Attributes:
        arguments (str): The arguments to be passed to the function.
        name (str): The name of the function.
    """

    arguments: str
    name: str


class Message(BaseModel):
    """Message by chat completion.

    Attributes:
        content (str): The content of the message.
        name (str, optional): The name of the message. Defaults to None.
        function_call (FunctionCall, optional): The function call. Defaults to
            None.
        role (Role): The role of the message.
    """

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
    """Message choice by chat completion.

    Attributes:
        finish_reason (FinishReason): The finish reason.
        index (int): The index of the message.
        message (Message): The message.
    """

    finish_reason: FinishReason
    index: int
    message: Message


class Usage(BaseModel):
    """Token usage by chat completion.

    Attributes:
        completion_tokens (int): The number of completion tokens.
        prompt_tokens (int): The number of prompt tokens.
        total_tokens (int): The number of total tokens.
    """

    completion_tokens: int
    prompt_tokens: int
    total_tokens: int


class Chatcmpl(BaseModel):
    """Chat completion response by OpenAI API.

    Attributes:
        choices (List[Choice]): The choices.
        created (int): The created timestamp.
        model (str): The model.
        object (str): The object.
        usage (Usage): The usage.
    """

    id: str
    choices: List[Choice]
    created: int
    model: str
    object: str
    usage: Usage


class FunctionCallRequest(BaseModel):
    """Function call for chat completion to call.

    Attributes:
        auto (bool): Whether to automatically call the function.
        name (str): The name of the function to call.
    """

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
    """Function parameter.

    Attributes:
        type (str): The type of the parameter.
        description (str): The description of the parameter.
        enum (Optional[List[str]]): The enum of the parameter. Defaults to
            None.
        required (bool): Whether the parameter is required.
    """

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
    """Parameters for function.

    Attributes:
        parameters (Dict[str, Parameter]): The parameters.
    """

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
    """Function.

    Attributes:
        description (str): The description of the function.
        name (str): The name of the function.
        parameters (Parameters): The parameters of the function.
    """

    description: str
    name: str
    parameters: Parameters


class ChatcmplRequest(BaseModel):
    """Chat completion request body.

    Attributes:
        deployment_id (str): The deployment ID. Defaults to config.
        model (str): The model. Defaults to config.
        messages (List[Message]): The messages.
        frequency_penalty (float): The frequency penalty. Defaults to 0.0.
        function_call (FunctionCallRequest): The function call. Defaults to
            None.
        functions (Optional[List[Function]]): The functions. Defaults to None.
        max_tokens (int): The maximum number of tokens. Defaults to 2048.
        n (int): The number of responses to return. Defaults to 1.
        presence_penalty (float): The presence penalty. Defaults to 0.0.
        stop (Optional[str | List[str]]): The stop. Defaults to None.
        stream (bool): Whether to stream the response. Defaults to False.
        temperature (float): The temperature. Defaults to 1.0.
        top_p (float): The top p. Defaults to 1.0.
        user (Optional[str]): The user. Defaults to None.
    """

    # containment: not contained
    deployment_id: str = Field(openai_config.deployment)
    model: str = Field(openai_config.model)
    # containment: else
    # deployment_id: Optional[str] = Field(None)
    # model: Optional[str] = Field(None)
    # containment: end
    messages: List[Message]
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
