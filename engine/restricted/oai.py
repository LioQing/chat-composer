import logging
from typing import Any, Dict, Optional

import openai

from config.logger import logger_config
from config.openai import openai_config
from core import models as core_models
from engine.oai.models import Chatcmpl
from oai import models

openai.api_key = openai_config.key
openai.api_base = openai_config.url
openai.api_type = openai_config.api_type
openai.api_version = openai_config.version


logger = logging.getLogger(__name__)
logger.setLevel(logger_config.level)


_current_component: Optional[core_models.Component] = None


class _CurrentComponentHelper:
    """Helper class for setting current component"""

    def __init__(self, component: core_models.Component):
        """Initialize the helper"""
        self.component = component

    def __enter__(self):
        """Enter the context"""
        global _current_component
        _current_component = self.component

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the context"""
        global _current_component
        _current_component = None


def init_oai(
    component: core_models.Component,
) -> _CurrentComponentHelper:
    """Set the current component"""
    return _CurrentComponentHelper(component)


openai_chatcmpl = openai.ChatCompletion.create


def create_chatcmpl_models(request: Dict[str, Any], response: Chatcmpl):
    """Create a Chatcmpl models from the request and response"""
    if _current_component is None:
        raise ValueError("current_component is None")

    chatcmpl_request = models.ChatcmplRequest.objects.create(
        response=models.Chatcmpl.objects.create(
            id=response.id,
            created=response.created,
            model=response.model,
            object=response.object,
            usage=models.Usage.objects.create(
                completion_tokens=response.usage.completion_tokens,
                prompt_tokens=response.usage.prompt_tokens,
                total_tokens=response.usage.total_tokens,
            ),
        ),
        request=request,
        component=_current_component,
    )

    chatcmpl = chatcmpl_request.response

    for choice in response.choices:
        models.Choice.objects.create(
            chatcmpl=chatcmpl,
            finish_reason=choice.finish_reason,
            index=choice.index,
            message=models.Message.objects.create(
                content=choice.message.content,
                name=choice.message.name,
                function_call=models.FunctionCall.objects.create(
                    arguments=choice.message.function_call.arguments,
                    name=choice.message.function_call.name,
                )
                if choice.message.function_call is not None
                else None,
                role=choice.message.role,
            ),
        )
