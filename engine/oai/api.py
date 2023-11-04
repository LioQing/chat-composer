def chatcmpl(request):
    """Call the OpenAI chat completion with the given request"""
    import openai

    from engine.restricted.oai import create_chatcmpl_models, logger

    from .models import Chatcmpl, ChatcmplRequest

    request: ChatcmplRequest = request
    request = request.model_dump()

    logger.debug(f"Calling OpenAI chat completion with request: {request}")

    response = openai.ChatCompletion.create(**request)
    response = Chatcmpl(**response)

    logger.debug(f"API response: {response}")

    create_chatcmpl_models(request, response)

    return response


def chatcmpl_with_messages(messages: list):
    """Call the OpenAI chat completion with the given messages"""
    from typing import List

    from config.openai import openai_config
    from engine.restricted.oai import logger

    from .models import ChatcmplRequest, Message

    messages: List[Message] = messages

    request = ChatcmplRequest(
        deployment_id=openai_config.deployment,
        model=openai_config.model,
        messages=messages,
    )

    response = chatcmpl(request)

    if response.choices[0].message.content is None:
        logger.error("API response message is None")
        raise ValueError("API response message is None")

    return response


def chatcmpl_function(function, messages: list = []):
    """Call the OpenAI chat completion to provide arguments for the function"""
    from typing import List

    from config.openai import openai_config
    from engine.restricted.oai import logger

    from .models import ChatcmplRequest, Function, FunctionCallRequest, Message

    function: Function = function
    messages: List[Message] = messages

    request = ChatcmplRequest(
        deployment_id=openai_config.deployment,
        model=openai_config.model,
        messages=messages,
        functions=[function],
        function_call=FunctionCallRequest(name=function.name),
    )

    response = chatcmpl(request)

    if response.choices[0].message.function_call is None:
        logger.error("API Function is not called.")
        raise ValueError("API Function is not called.")

    return response
