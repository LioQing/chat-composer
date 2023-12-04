import copy
import logging
from typing import Any, Dict

from django.db.models import QuerySet

from core import exceptions, models

from . import oai


def run(pipeline: models.Pipeline, user_message: str) -> Dict[str, Any]:
    """Run the pipeline"""
    logger = logging.getLogger(__name__)

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
    logger.info(f"Running component {component.name}")
    logger.debug(f"Code:\n{component.code}")

    with oai.init(component):
        # Compile the code
        byte_code = compile(
            component.code, f"{component.function_name}.py", "exec"
        )

        loc = {}

        glob = {}
        glob["__name__"] = f"pipeline {pipeline.id} component {component.id}"
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

    return new_data
