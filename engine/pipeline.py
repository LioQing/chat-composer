import copy
import logging
from typing import Any, Dict

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
from RestrictedPython.Guards import guarded_iter_unpack_sequence, safer_getattr

from config.logger import logger_config
from core import exceptions, models

from . import openai


def run(pipeline: models.Pipeline, user_message: str) -> Dict[str, Any]:
    """Run the pipeline"""
    logger = logging.getLogger(__name__)
    logger.setLevel(logger_config.level)
    logger.info(f"Running pipeline {pipeline.name}")

    data = {}
    for component in pipeline.components.order_by("order").all():
        data = run_component(component, user_message, data)

    logger.info(f"Finished running pipeline {pipeline.name}")
    return data


def run_component(
    component: models.Component,
    user_message: str,
    data: Dict[str, Any],
) -> Dict[str, Any]:
    """Run a component"""
    logger = logging.getLogger(__name__)
    logger.setLevel(logger_config.level)
    logger.info(f"Running component {component.name}")
    logger.debug(component.code)

    # Compile the code
    byte_code = compile_restricted(
        component.code, f"<{component.name}>", "exec"
    )

    state = copy.deepcopy(component.state)
    loc = {"state": state}

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
    glob["getattr"] = safer_getattr
    glob["openai"] = openai

    exec(byte_code, glob, loc)

    # Run the code
    logger.debug(f"data: {data}, state: {component.state}")

    new_data = loc[component.name](user_message, data)
    component.state = loc["state"]

    logger.debug(f"data: {new_data}, state: {component.state}")
    logger.info(f"Finished running component {component.name}")

    # Validation
    if not isinstance(new_data, dict):
        raise exceptions.InvalidComponentCode(
            f"Component {component.name} did not return a dict"
        )

    if not isinstance(component.state, dict):
        raise exceptions.InvalidComponentCode(
            f"Component {component.name} did not set a dict for state"
        )

    return new_data
