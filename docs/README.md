<!-- markdownlint-disable -->

# Pipeline

Pipeline in this context is a sequence of components chained together.

The components are called in the order they are defined in the pipeline.

# Component

Components are the building blocks of the pipeline. They provide the functionality to the pipeline.

- **State**: persistent JSON object that is stored in the component.
- **Pipeline State**: persistent JSON object that is stored in the pipeline.
- **Code**: Python code in which the defined function is executed.

## State

The state is a persistent JSON object stored in the component.

It is not accessible to other components.

It can be globally accessed and modified by the code of the component by using the identifier <b>`state`</b>.

## Pipeline State

The pipeline state is a persistent JSON object stored in the pipeline.

It is accessible to all the components in the pipeline.

It can be globally accessed and modified by the code of the component by using the identifier <b>`pstate`</b>.

## Code

The code is a Python code in which the defined function is executed.

The code must contain a function matching the function name defined in the component to be called.

You may use any API provided by the modules listed in the [API](#api) section. You may also access the global dictionaries <b>`state`</b> and <b>`pstate`</b> to access and modify the state and pipeline state respectively.

The function must have the following signature:

```python
def function_name(user_message, data):
    ...
    return new_data
```

***Args:***

- <b>`user_message`</b> (str): The message sent by the user.
- <b>`data`</b> (dict): The data passed from the previous component.

***Returns:***

- <b>`dict`</b>: The data to be passed to the next component.

_Note: the python code is executed by [RestrictedPython](https://restrictedpython.readthedocs.io/en/latest/) with all the [restricted builtins](https://restrictedpython.readthedocs.io/en/latest/usage/api.html#restricted-builtins) provided._

# Modules

These are the modules that can be used in the code of the components.

All models in the API modules are JSON serializable but not deserializable.
However, you can create the model by unpacking them into the constructor.

- [`oai`](./oai/README.md): OpenAI module.
