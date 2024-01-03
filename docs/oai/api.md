<!-- markdownlint-disable -->

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/oai/api.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `oai.api`
OpenAI API functions.


---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/oai/api.py#L11"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `chatcmpl`

```python
chatcmpl(request: oai.models.ChatcmplRequest) → Chatcmpl
```

Call the OpenAI chat completion with the given request.

The request and response are logged to the database.



**Args:**

 - <b>`request`</b> (models.ChatcmplRequest):  The request to be sent to the API.



**Returns:**

 - <b>`models.Chatcmpl`</b>:  The response from the API.




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
