<!-- markdownlint-disable -->

# `oai` Overview

## Modules

- [`api`](./api.md#module-engineoaiapi): OpenAI API functions.
- [`enums`](./enums.md#module-engineoaienums): Enumerations for OpenAI API.
- [`models`](./models.md#module-engineoaimodels): Models for OpenAI API.

## Classes

- [`enums.FinishReason`](./enums.md#class-finishreason): Finish reason enumeration for conversation messages.
- [`enums.Role`](./enums.md#class-role): Role enumeration for conversation messages.
- [`models.Chatcmpl`](./models.md#class-chatcmpl): Chat completion response by OpenAI API.
- [`models.ChatcmplRequest`](./models.md#class-chatcmplrequest): Chat completion request body.
- [`models.Choice`](./models.md#class-choice): Message choice by chat completion.
- [`models.Function`](./models.md#class-function): Function.
- [`models.FunctionCall`](./models.md#class-functioncall): Function call by chat completion.
- [`models.FunctionCallRequest`](./models.md#class-functioncallrequest): Function call for chat completion to call.
- [`models.Message`](./models.md#class-message): Message by chat completion.
- [`models.Parameter`](./models.md#class-parameter): Function parameter.
- [`models.Parameters`](./models.md#class-parameters): Parameters for function.
- [`models.Usage`](./models.md#class-usage): Token usage by chat completion.

## Functions

- [`api.chatcmpl`](./api.md#function-chatcmpl): Call the OpenAI chat completion with the given request.
- [`api.chatcmpl_function`](./api.md#function-chatcmpl_function): Call the OpenAI chat completion to provide arguments for the function.
- [`api.chatcmpl_with_messages`](./api.md#function-chatcmpl_with_messages): Call the OpenAI chat completion with the given messages.


---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
