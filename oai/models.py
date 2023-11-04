from django.db import models

from . import enums


class FunctionCall(models.Model):
    """Function call"""

    arguments = models.CharField()
    name = models.CharField()


class Message(models.Model):
    """Message for conversation"""

    content = models.CharField()
    name = models.CharField(null=True, blank=True)
    function_call = models.OneToOneField(
        FunctionCall, on_delete=models.CASCADE, null=True, blank=True
    )
    role = models.CharField()


class Choice(models.Model):
    """Message choice by OpenAI API"""

    chatcmpl = models.ForeignKey("Chatcmpl", on_delete=models.CASCADE)
    finish_reason = models.CharField(choices=enums.FinishReason.choices())
    index = models.PositiveIntegerField()
    message = models.OneToOneField(Message, on_delete=models.CASCADE)


class Usage(models.Model):
    """Usage by OpenAI API"""

    completion_tokens = models.PositiveIntegerField()
    prompt_tokens = models.PositiveIntegerField()
    total_tokens = models.PositiveIntegerField()


class Chatcmpl(models.Model):
    """Chat completion by OpenAI API"""

    id = models.CharField(primary_key=True)
    created = models.PositiveIntegerField()
    model = models.CharField()
    object = models.CharField()
    usage = models.OneToOneField(Usage, on_delete=models.CASCADE)


class ChatcmplRequest(models.Model):
    """Chat completion request for OpenAI API"""

    request = models.JSONField()
    response = models.OneToOneField(Chatcmpl, on_delete=models.CASCADE)
    component = models.ForeignKey("core.Component", on_delete=models.CASCADE)
