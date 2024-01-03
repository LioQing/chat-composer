<!-- markdownlint-disable -->

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/vai/enums.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `vai.enums`
Enumerations for Vertex AI API.



---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/vai/enums.py#L6"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GeminiRole`
Role of the content in Gemini API



**Attributes:**

 - <b>`USER`</b>:  The user.
 - <b>`MODEL`</b>:  The model.





---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/vai/enums.py#L18"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GeminiHarmCategory`
The category of a rating.



**Attributes:**
  HARM_CATEGORY_UNSPECIFIED (0):  Category is unspecified.  HARM_CATEGORY_DEROGATORY (1):  Negative or harmful comments targeting  identity and/or protected attribute.  HARM_CATEGORY_TOXICITY (2):  Content that is rude, disrepspectful, or  profane.  HARM_CATEGORY_VIOLENCE (3):  Describes scenarios depictng violence against  an individual or group, or general descriptions  of gore.  HARM_CATEGORY_SEXUAL (4):  Contains references to sexual acts or other  lewd content.  HARM_CATEGORY_MEDICAL (5):  Promotes unchecked medical advice.  HARM_CATEGORY_DANGEROUS (6):  Dangerous content that promotes, facilitates,  or encourages harmful acts.  HARM_CATEGORY_HARASSMENT (7):  Harasment content.  HARM_CATEGORY_HATE_SPEECH (8):  Hate speech and content.  HARM_CATEGORY_SEXUALLY_EXPLICIT (9):  Sexually explicit content.  HARM_CATEGORY_DANGEROUS_CONTENT (10):  Dangerous content.





---

<a href="https://github.com/LioQing/chat-composer/blob/main/engine/vai/enums.py#L65"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GeminiHarmBlockThreshold`
Block at and beyond a specified harm probability.



**Attributes:**
  HARM_BLOCK_THRESHOLD_UNSPECIFIED (0):  Threshold is unspecified.  BLOCK_LOW_AND_ABOVE (1):  Content with NEGLIGIBLE will be allowed.  BLOCK_MEDIUM_AND_ABOVE (2):  Content with NEGLIGIBLE and LOW will be  allowed.  BLOCK_ONLY_HIGH (3):  Content with NEGLIGIBLE, LOW, and MEDIUM will  be allowed.  BLOCK_NONE (4):  All content will be allowed.







---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
