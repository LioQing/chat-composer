import copy
import logging
from typing import Any, Dict

from django.db.models import QuerySet
from RestrictedPython import (
    compile_restricted,
    limited_builtins,
    safe_builtins,
    utility_builtins,
)
from RestrictedPython.Eval import (
    default_guarded_getitem,
    default_guarded_getiter,
)
from RestrictedPython.Guards import (
    full_write_guard,
    guarded_iter_unpack_sequence,
    guarded_unpack_sequence,
)

import engine.restricted.oai
from config.logger import logger_config
from core import exceptions, models

from . import oai


def run(pipeline: models.Pipeline, user_message: str) -> Dict[str, Any]:
    """Run the pipeline"""
    logger = logging.getLogger(__name__)
    logger.setLevel(logger_config.level)
    logger.info(f"Running pipeline {pipeline.name}")

    data = {}
    component_instances: QuerySet = pipeline.componentinstance_set
    for component_instance in component_instances.order_by("order").filter(
        is_enabled=True
    ):
        component_instance: models.ComponentInstance = component_instance
        data = run_component(
            component_instance.component, pipeline, user_message, data
        )

    logger.info(f"Finished running pipeline {pipeline.name}")
    return data


def run_component(
    component: models.Component,
    pipeline: models.Pipeline,
    user_message: str,
    data: Dict[str, Any],
) -> Dict[str, Any]:
    """Run a component"""
    logger = logging.getLogger(__name__)
    logger.setLevel(logger_config.level)
    logger.info(f"Running component {component.name}")
    logger.debug(component.code)

    # Setup
    engine.restricted.oai.current_component = component

    # Compile the code
    byte_code = compile_restricted(
        component.code, f"{component.function_name}.py", "exec"
    )

    loc = {}

    builtins = {}
    builtins.update(safe_builtins)
    builtins.update(limited_builtins)
    builtins.update(utility_builtins)

    glob = {}
    glob["__builtins__"] = builtins
    glob["__metaclass__"] = type
    glob["__name__"] = "restricted namespace"
    glob["_getiter_"] = default_guarded_getiter
    glob["_getitem_"] = default_guarded_getitem
    glob["_iter_unpack_sequence_"] = guarded_iter_unpack_sequence
    glob["_unpack_sequence_"] = guarded_unpack_sequence
    glob["_write_"] = full_write_guard

    glob["pstate"] = copy.deepcopy(pipeline.state)
    glob["state"] = copy.deepcopy(component.state)
    glob["oai"] = oai

    exec(byte_code, glob, loc)

    # Run the code
    logger.debug(
        f"\ndata:\n{data}\n\nstate:\n{component.state}\n\n"
        f"pstate:{pipeline.state}"
    )

    function = loc[component.function_name]
    new_data = function(user_message, data)
    component.state = glob["state"]
    pipeline.state = glob["pstate"]

    logger.debug(
        f"\ndata:\n{new_data}\n\nstate:\n{component.state}\n\n"
        f"pstate:{pipeline.state}"
    )

    # Validation
    if not isinstance(component.state, dict):
        raise exceptions.InvalidComponentCode(
            f"Component {component.name} did not set a dict for state"
        )

    if not isinstance(pipeline.state, dict):
        raise exceptions.InvalidComponentCode(
            f"Component {component.name} did not set a dict for pstate"
        )

    # Save
    component.save()
    pipeline.save()
    logger.info(f"Finished running component {component.name}")

    # Validation
    if not isinstance(new_data, dict):
        raise exceptions.InvalidComponentCode(
            f"Component {component.name} did not return a dict"
        )

    # Clean up
    engine.restricted.oai.current_component = None

    return new_data
