<!-- markdownlint-disable -->

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/oai/models.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `oai.models`
Models for OpenAI API.



---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/oai/models.py#L14"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FunctionCall`
Function call by chat completion.



**Attributes:**

 - <b>`arguments`</b> (str):  The arguments to be passed to the function.
 - <b>`name`</b> (str):  The name of the function.


---

#### <kbd>property</kbd> FunctionCall.model_computed_fields

Get the computed fields of this model instance.



**Returns:**
  A dictionary of computed field names and their corresponding `ComputedFieldInfo` objects.

---

#### <kbd>property</kbd> FunctionCall.model_extra

Get extra fields set during validation.



**Returns:**
  A dictionary of extra fields, or `None` if `config.extra` is not set to `"allow"`.

---

#### <kbd>property</kbd> FunctionCall.model_fields_set

Returns the set of fields that have been set on this model instance.



**Returns:**
  A set of strings representing the fields that have been set,  i.e. that were not filled from defaults.




---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/oai/models.py#L26"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Message`
Message by chat completion.



**Attributes:**

 - <b>`content`</b> (str):  The content of the message.
 - <b>`name`</b> (str, optional):  The name of the message. Defaults to None.
 - <b>`function_call`</b> (FunctionCall, optional):  The function call. Defaults to  None.
 - <b>`role`</b> (Role):  The role of the message.


---

#### <kbd>property</kbd> Message.model_computed_fields

Get the computed fields of this model instance.



**Returns:**
  A dictionary of computed field names and their corresponding `ComputedFieldInfo` objects.

---

#### <kbd>property</kbd> Message.model_extra

Get extra fields set during validation.



**Returns:**
  A dictionary of extra fields, or `None` if `config.extra` is not set to `"allow"`.

---

#### <kbd>property</kbd> Message.model_fields_set

Returns the set of fields that have been set on this model instance.



**Returns:**
  A set of strings representing the fields that have been set,  i.e. that were not filled from defaults.



---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/oai/models.py#L42"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `Message.model_dump`

```python
model_dump() → Dict[str, Any]
```

Dump the model


---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/oai/models.py#L56"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Choice`
Message choice by chat completion.



**Attributes:**

 - <b>`finish_reason`</b> (FinishReason):  The finish reason.
 - <b>`index`</b> (int):  The index of the message.
 - <b>`message`</b> (Message):  The message.


---

#### <kbd>property</kbd> Choice.model_computed_fields

Get the computed fields of this model instance.



**Returns:**
  A dictionary of computed field names and their corresponding `ComputedFieldInfo` objects.

---

#### <kbd>property</kbd> Choice.model_extra

Get extra fields set during validation.



**Returns:**
  A dictionary of extra fields, or `None` if `config.extra` is not set to `"allow"`.

---

#### <kbd>property</kbd> Choice.model_fields_set

Returns the set of fields that have been set on this model instance.



**Returns:**
  A set of strings representing the fields that have been set,  i.e. that were not filled from defaults.




---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/oai/models.py#L70"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Usage`
Token usage by chat completion.



**Attributes:**

 - <b>`completion_tokens`</b> (int):  The number of completion tokens.
 - <b>`prompt_tokens`</b> (int):  The number of prompt tokens.
 - <b>`total_tokens`</b> (int):  The number of total tokens.


---

#### <kbd>property</kbd> Usage.model_computed_fields

Get the computed fields of this model instance.



**Returns:**
  A dictionary of computed field names and their corresponding `ComputedFieldInfo` objects.

---

#### <kbd>property</kbd> Usage.model_extra

Get extra fields set during validation.



**Returns:**
  A dictionary of extra fields, or `None` if `config.extra` is not set to `"allow"`.

---

#### <kbd>property</kbd> Usage.model_fields_set

Returns the set of fields that have been set on this model instance.



**Returns:**
  A set of strings representing the fields that have been set,  i.e. that were not filled from defaults.




---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/oai/models.py#L84"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Chatcmpl`
Chat completion response by OpenAI API.



**Attributes:**

 - <b>`choices`</b> (List[Choice]):  The choices.
 - <b>`created`</b> (int):  The created timestamp.
 - <b>`model`</b> (str):  The model.
 - <b>`object`</b> (str):  The object.
 - <b>`usage`</b> (Usage):  The usage.


---

#### <kbd>property</kbd> Chatcmpl.model_computed_fields

Get the computed fields of this model instance.



**Returns:**
  A dictionary of computed field names and their corresponding `ComputedFieldInfo` objects.

---

#### <kbd>property</kbd> Chatcmpl.model_extra

Get extra fields set during validation.



**Returns:**
  A dictionary of extra fields, or `None` if `config.extra` is not set to `"allow"`.

---

#### <kbd>property</kbd> Chatcmpl.model_fields_set

Returns the set of fields that have been set on this model instance.



**Returns:**
  A set of strings representing the fields that have been set,  i.e. that were not filled from defaults.




---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/oai/models.py#L103"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FunctionCallRequest`
Function call for chat completion to call.

If you wish to use auto or none, simply supply them as strings to the ChatcmplRequest.



**Attributes:**

 - <b>`name`</b> (str):  The name of the function to call.


---

#### <kbd>property</kbd> FunctionCallRequest.model_computed_fields

Get the computed fields of this model instance.



**Returns:**
  A dictionary of computed field names and their corresponding `ComputedFieldInfo` objects.

---

#### <kbd>property</kbd> FunctionCallRequest.model_extra

Get extra fields set during validation.



**Returns:**
  A dictionary of extra fields, or `None` if `config.extra` is not set to `"allow"`.

---

#### <kbd>property</kbd> FunctionCallRequest.model_fields_set

Returns the set of fields that have been set on this model instance.



**Returns:**
  A set of strings representing the fields that have been set,  i.e. that were not filled from defaults.




---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/oai/models.py#L116"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Parameter`
Function parameter.



**Attributes:**

 - <b>`type`</b> (str):  The type of the parameter.
 - <b>`description`</b> (str):  The description of the parameter.
 - <b>`enum`</b> (Optional[List[str]]):  The enum of the parameter. Defaults to  None.
 - <b>`required`</b> (bool):  Whether the parameter is required.


---

#### <kbd>property</kbd> Parameter.model_computed_fields

Get the computed fields of this model instance.



**Returns:**
  A dictionary of computed field names and their corresponding `ComputedFieldInfo` objects.

---

#### <kbd>property</kbd> Parameter.model_extra

Get extra fields set during validation.



**Returns:**
  A dictionary of extra fields, or `None` if `config.extra` is not set to `"allow"`.

---

#### <kbd>property</kbd> Parameter.model_fields_set

Returns the set of fields that have been set on this model instance.



**Returns:**
  A set of strings representing the fields that have been set,  i.e. that were not filled from defaults.



---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/oai/models.py#L132"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `Parameter.model_dump`

```python
model_dump() → Dict[str, Any]
```

Dump the model


---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/oai/models.py#L143"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Parameters`
Parameters for function.



**Attributes:**

 - <b>`parameters`</b> (Dict[str, Parameter]):  The parameters.


---

#### <kbd>property</kbd> Parameters.model_computed_fields

Get the computed fields of this model instance.



**Returns:**
  A dictionary of computed field names and their corresponding `ComputedFieldInfo` objects.

---

#### <kbd>property</kbd> Parameters.model_extra

Get extra fields set during validation.



**Returns:**
  A dictionary of extra fields, or `None` if `config.extra` is not set to `"allow"`.

---

#### <kbd>property</kbd> Parameters.model_fields_set

Returns the set of fields that have been set on this model instance.



**Returns:**
  A set of strings representing the fields that have been set,  i.e. that were not filled from defaults.



---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/oai/models.py#L152"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `Parameters.model_dump`

```python
model_dump() → Dict[str, Any]
```

Dump the model


---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/oai/models.py#L168"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Function`
Function.



**Attributes:**

 - <b>`description`</b> (str):  The description of the function.
 - <b>`name`</b> (str):  The name of the function.
 - <b>`parameters`</b> (Parameters):  The parameters of the function.


---

#### <kbd>property</kbd> Function.model_computed_fields

Get the computed fields of this model instance.



**Returns:**
  A dictionary of computed field names and their corresponding `ComputedFieldInfo` objects.

---

#### <kbd>property</kbd> Function.model_extra

Get extra fields set during validation.



**Returns:**
  A dictionary of extra fields, or `None` if `config.extra` is not set to `"allow"`.

---

#### <kbd>property</kbd> Function.model_fields_set

Returns the set of fields that have been set on this model instance.



**Returns:**
  A set of strings representing the fields that have been set,  i.e. that were not filled from defaults.




---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/oai/models.py#L182"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ChatcmplRequest`
Chat completion request body.



**Attributes:**

 - <b>`deployment_id`</b> (str):  The deployment ID. Defaults to config.
 - <b>`model`</b> (str):  The model. Defaults to config.
 - <b>`messages`</b> (List[Message]):  The messages.
 - <b>`frequency_penalty`</b> (float):  The frequency penalty. Defaults to 0.0.
 - <b>`function_call`</b> (FunctionCallRequest):  The function call. Defaults to  None.
 - <b>`functions`</b> (Optional[List[Function]]):  The functions. Defaults to None.
 - <b>`max_tokens`</b> (int):  The maximum number of tokens. Defaults to 2048.
 - <b>`n`</b> (int):  The number of responses to return. Defaults to 1.
 - <b>`presence_penalty`</b> (float):  The presence penalty. Defaults to 0.0.
 - <b>`stop`</b> (Optional[str | List[str]]):  The stop. Defaults to None.
 - <b>`stream`</b> (bool):  Whether to stream the response. Defaults to False.
 - <b>`temperature`</b> (float):  The temperature. Defaults to 1.0.
 - <b>`top_p`</b> (float):  The top p. Defaults to 1.0.
 - <b>`user`</b> (Optional[str]):  The user. Defaults to None.


---

#### <kbd>property</kbd> ChatcmplRequest.model_computed_fields

Get the computed fields of this model instance.



**Returns:**
  A dictionary of computed field names and their corresponding `ComputedFieldInfo` objects.

---

#### <kbd>property</kbd> ChatcmplRequest.model_extra

Get extra fields set during validation.



**Returns:**
  A dictionary of extra fields, or `None` if `config.extra` is not set to `"allow"`.

---

#### <kbd>property</kbd> ChatcmplRequest.model_fields_set

Returns the set of fields that have been set on this model instance.



**Returns:**
  A set of strings representing the fields that have been set,  i.e. that were not filled from defaults.



---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/oai/models.py#L225"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ChatcmplRequest.model_dump`

```python
model_dump() → Dict[str, Any]
```

Dump the model




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
