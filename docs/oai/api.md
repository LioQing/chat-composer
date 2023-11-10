<!-- markdownlint-disable -->

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/oai/api.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `oai.api`
OpenAI API functions.


---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/oai/api.py#L4"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `chatcmpl`

```python
chatcmpl(request)
```

Call the OpenAI chat completion with the given request.

The request and response are logged to the database.



**Args:**

 - <b>`request`</b> (models.ChatcmplRequest):  The request to be sent to the API.



**Returns:**

 - <b>`models.Chatcmpl`</b>:  The response from the API.


---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/oai/api.py#L36"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `chatcmpl_with_messages`

```python
chatcmpl_with_messages(messages: list)
```

Call the OpenAI chat completion with the given messages.



**Args:**

 - <b>`messages`</b> (List[models.Message]):  A list of messages to be sent to the  API.



**Returns:**

 - <b>`models.Chatcmpl`</b>:  The response from the API.


---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/oai/api.py#L70"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `chatcmpl_function`

```python
chatcmpl_function(function, messages: list = [])
```

Call the OpenAI chat completion to provide arguments for the function.



**Args:**

 - <b>`function`</b> (models.Function):  The function to be called.
 - <b>`messages`</b> (List[models.Message], optional):  A list of messages to be  sent to the API. Defaults to [].



**Returns:**

 - <b>`models.Chatcmpl`</b>:  The response from the API.




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
