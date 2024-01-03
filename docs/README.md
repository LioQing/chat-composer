<!-- markdownlint-disable -->

# Pipeline

Pipeline in this context is a sequence of components chained together.

The components are called in the order they are defined in the pipeline.

# Component

Components are the building blocks of the pipeline. They provide the functionality to the pipeline.

## State

The state is a persistent JSON object stored in the component.

It is accessed using the `component_state` function in the module [Composer module](./composer/README.md).

## Pipeline State

The pipeline state is a persistent JSON object stored in the pipeline.

It is accessed using the `pipeline_state` function in the module [Composer module](./composer/README.md).

## Code

The code is a Python code in which the defined function is executed.

The code must contain a function matching the function name defined in the component to be called.

You may use any API provided by the modules listed in the [Modules](#modules) section.

# Modules

These are the modules that can be used in the code of the components.

All models in the API modules are JSON serializable but not deserializable.
However, you can create the model by unpacking them into the constructor.

- [`composer`](./composer/README.md): Composer module.
- [`oai`](./oai/README.md): OpenAI module.
- [`vai`](./vai/README.md): Google Vertex AI module.
