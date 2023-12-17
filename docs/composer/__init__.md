<!-- markdownlint-disable -->

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/composer/__init__.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `composer`
Chat Composer module.


---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/composer/__init__.py#L25"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `url`

```python
url(path: str) → str
```

Get the composer URL for the given path.


---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/composer/__init__.py#L31"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `access`

```python
access() → str
```

Get the composer token.


---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/composer/__init__.py#L41"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `refresh`

```python
refresh() → str
```

Get the composer token.


---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/composer/__init__.py#L51"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `component_id`

```python
component_id() → int
```

Get the current component ID.


---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/composer/__init__.py#L59"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `pipeline_id`

```python
pipeline_id() → int
```

Get the current pipeline ID.


---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/composer/__init__.py#L67"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `component_state`

```python
component_state(id: Optional[int] = None) → Dict[str, Any]
```

Get the state of the component with the given ID.


---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/composer/__init__.py#L82"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `pipeline_state`

```python
pipeline_state() → Dict[str, Any]
```

Get the state of the pipeline.


---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/composer/__init__.py#L199"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `init_pipeline`

```python
init_pipeline(pipeline_id: int, user_message: str) → CurrentPipelineHelper
```

Set the current pipeline


---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/composer/__init__.py#L206"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `init_component`

```python
init_component(component_id: int) → CurrentComponentHelper
```

Set the current component


---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/composer/__init__.py#L11"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ComponentState`
State of a component.


---

#### <kbd>property</kbd> ComponentState.model_computed_fields

Get the computed fields of this model instance.



**Returns:**
  A dictionary of computed field names and their corresponding `ComputedFieldInfo` objects.

---

#### <kbd>property</kbd> ComponentState.model_extra

Get extra fields set during validation.



**Returns:**
  A dictionary of extra fields, or `None` if `config.extra` is not set to `"allow"`.

---

#### <kbd>property</kbd> ComponentState.model_fields_set

Returns the set of fields that have been set on this model instance.



**Returns:**
  A set of strings representing the fields that have been set,  i.e. that were not filled from defaults.




---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/composer/__init__.py#L18"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `States`
States of components and pipeline.


---

#### <kbd>property</kbd> States.model_computed_fields

Get the computed fields of this model instance.



**Returns:**
  A dictionary of computed field names and their corresponding `ComputedFieldInfo` objects.

---

#### <kbd>property</kbd> States.model_extra

Get extra fields set during validation.



**Returns:**
  A dictionary of extra fields, or `None` if `config.extra` is not set to `"allow"`.

---

#### <kbd>property</kbd> States.model_fields_set

Returns the set of fields that have been set on this model instance.



**Returns:**
  A set of strings representing the fields that have been set,  i.e. that were not filled from defaults.




---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/composer/__init__.py#L95"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CurrentPipelineHelper`
Helper class for setting current pipeline.

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/composer/__init__.py#L98"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CurrentPipelineHelper.__init__`

```python
__init__(pipeline_id: int, user_message: str)
```

Initialize the helper




---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/composer/__init__.py#L176"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CurrentPipelineHelper.set_response`

```python
set_response(response: Any)
```

Set the response


---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/composer/__init__.py#L181"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CurrentComponentHelper`
Helper class for setting current component.

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/composer/__init__.py#L184"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CurrentComponentHelper.__init__`

```python
__init__(component_id: int)
```

Initialize the helper







---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
