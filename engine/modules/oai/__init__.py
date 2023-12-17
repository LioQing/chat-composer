"""OpenAI module."""

from . import api, enums, models  # noqa: F401

# containment: not contained
import logging
from typing import Any, Dict

import openai

from config.openai import openai_config
from core import models as core_models
from engine.modules.oai.models import Chatcmpl
from engine.modules.composer import component_id
from oai import models as django_models

openai.api_key = openai_config.key
openai.api_base = openai_config.url
openai.api_type = openai_config.api_type
openai.api_version = openai_config.version


logger = logging.getLogger(__name__)


openai_chatcmpl = openai.ChatCompletion.create


def create_chatcmpl_models(request: Dict[str, Any], response: Chatcmpl):
    """Create a Chatcmpl models from the request and response"""
    current_component = core_models.Component.objects.get(id=component_id())

    chatcmpl_request = django_models.ChatcmplRequest.objects.create(
        response=django_models.Chatcmpl.objects.create(
            id=response.id,
            created=response.created,
            model=response.model,
            object=response.object,
            usage=django_models.Usage.objects.create(
                completion_tokens=response.usage.completion_tokens,
                prompt_tokens=response.usage.prompt_tokens,
                total_tokens=response.usage.total_tokens,
            ),
        ),
        request=request,
        component=current_component,
    )

    chatcmpl = chatcmpl_request.response

    for choice in response.choices:
        django_models.Choice.objects.create(
            chatcmpl=chatcmpl,
            finish_reason=choice.finish_reason,
            index=choice.index,
            message=django_models.Message.objects.create(
                content=choice.message.content,
                name=choice.message.name,
                function_call=django_models.FunctionCall.objects.create(
                    arguments=choice.message.function_call.arguments,
                    name=choice.message.function_call.name,
                )
                if choice.message.function_call is not None
                else None,
                role=choice.message.role,
            ),
        )


# containment: end
