<!-- markdownlint-disable -->

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/vai/models.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `vai.models`
Models for Vertex AI API.

This module only defines the request models in Pydantic. The response models are defined in the Google API library `google.generativeai`, which is imported to this module as `google_types`.

For more details, see the `google.generativeai` documentation: https://ai.google.dev/docs.

And for more about the response type `GenerateContentResponse`, see: https://ai.google.dev/api/python/google/generativeai/types/GenerateContentResponse.



---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/vai/models.py#L21"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GeminiPart`
Gemini part.



**Attributes:**

 - <b>`text`</b> (str):  The text.


---

#### <kbd>property</kbd> GeminiPart.model_computed_fields

Get the computed fields of this model instance.



**Returns:**
  A dictionary of computed field names and their corresponding `ComputedFieldInfo` objects.

---

#### <kbd>property</kbd> GeminiPart.model_extra

Get extra fields set during validation.



**Returns:**
  A dictionary of extra fields, or `None` if `config.extra` is not set to `"allow"`.

---

#### <kbd>property</kbd> GeminiPart.model_fields_set

Returns the set of fields that have been set on this model instance.



**Returns:**
  A set of strings representing the fields that have been set,  i.e. that were not filled from defaults.




---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/vai/models.py#L31"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GeminiContent`
Gemini content.



**Attributes:**

 - <b>`parts`</b> (List[GeminiPart | str]):  The parts.
 - <b>`role`</b> (GeminiRole):  The role.


---

#### <kbd>property</kbd> GeminiContent.model_computed_fields

Get the computed fields of this model instance.



**Returns:**
  A dictionary of computed field names and their corresponding `ComputedFieldInfo` objects.

---

#### <kbd>property</kbd> GeminiContent.model_extra

Get extra fields set during validation.



**Returns:**
  A dictionary of extra fields, or `None` if `config.extra` is not set to `"allow"`.

---

#### <kbd>property</kbd> GeminiContent.model_fields_set

Returns the set of fields that have been set on this model instance.



**Returns:**
  A set of strings representing the fields that have been set,  i.e. that were not filled from defaults.




---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/vai/models.py#L43"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GeminiGenerationConfig`
Gemini generation configuration.



**Attributes:**

 - <b>`candidate_count`</b> (int):  The number of candidates to generate.
 - <b>`stop_sequences`</b> (List[str]):  The stop sequences.
 - <b>`max_tokens`</b> (int):  The maximum number of tokens to generate.
 - <b>`temperature`</b> (float):  The temperature.
 - <b>`top_p`</b> (Optional[float]):  The top p. Defaults to None.
 - <b>`top_k`</b> (Optional[int]):  The top k. Defaults to None.


---

#### <kbd>property</kbd> GeminiGenerationConfig.model_computed_fields

Get the computed fields of this model instance.



**Returns:**
  A dictionary of computed field names and their corresponding `ComputedFieldInfo` objects.

---

#### <kbd>property</kbd> GeminiGenerationConfig.model_extra

Get extra fields set during validation.



**Returns:**
  A dictionary of extra fields, or `None` if `config.extra` is not set to `"allow"`.

---

#### <kbd>property</kbd> GeminiGenerationConfig.model_fields_set

Returns the set of fields that have been set on this model instance.



**Returns:**
  A set of strings representing the fields that have been set,  i.e. that were not filled from defaults.



---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/vai/models.py#L62"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `GeminiGenerationConfig.model_dump`

```python
model_dump() → Dict[str, Any]
```

Dump the model to a dictionary.


---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/vai/models.py#L67"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GeminiSafetySetting`
Gemini safety setting.



**Attributes:**

 - <b>`harm_category`</b> (GeminiHarmCategory):  The harm category.
 - <b>`block_threshold`</b> (GeminiHarmBlockThreshold):  The block threshold.


---

#### <kbd>property</kbd> GeminiSafetySetting.model_computed_fields

Get the computed fields of this model instance.



**Returns:**
  A dictionary of computed field names and their corresponding `ComputedFieldInfo` objects.

---

#### <kbd>property</kbd> GeminiSafetySetting.model_extra

Get extra fields set during validation.



**Returns:**
  A dictionary of extra fields, or `None` if `config.extra` is not set to `"allow"`.

---

#### <kbd>property</kbd> GeminiSafetySetting.model_fields_set

Returns the set of fields that have been set on this model instance.



**Returns:**
  A set of strings representing the fields that have been set,  i.e. that were not filled from defaults.




---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/vai/models.py#L79"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GeminiRequest`
Gemini request body.



**Attributes:**

 - <b>`contents`</b> (GeminiContent | GeminiPart | str):  The content.
 - <b>`generation_config`</b> (Optional[GeminiGenerationConfig]):  The generation  configuration. Defaults to None.
 - <b>`safety_settings`</b> (Optional[GeminiSafetySetting]):  The safety  settings. Defaults to None.


---

#### <kbd>property</kbd> GeminiRequest.model_computed_fields

Get the computed fields of this model instance.



**Returns:**
  A dictionary of computed field names and their corresponding `ComputedFieldInfo` objects.

---

#### <kbd>property</kbd> GeminiRequest.model_extra

Get extra fields set during validation.



**Returns:**
  A dictionary of extra fields, or `None` if `config.extra` is not set to `"allow"`.

---

#### <kbd>property</kbd> GeminiRequest.model_fields_set

Returns the set of fields that have been set on this model instance.



**Returns:**
  A set of strings representing the fields that have been set,  i.e. that were not filled from defaults.






---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
