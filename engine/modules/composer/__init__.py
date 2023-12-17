"""Chat Composer module."""

import os
import traceback
from types import TracebackType
import requests
from typing import Any, Dict, List, Optional, Type
from pydantic import BaseModel


class ComponentState(BaseModel):
    """State of a component."""

    id: int
    state: Dict[str, Any]


class States(BaseModel):
    """States of components and pipeline."""

    component_states: List[ComponentState]
    pipeline_state: Dict[str, Any]


def url(path: str) -> str:
    """Get the composer URL for the given path."""
    port = os.environ.get("CHAT_COMPOSER_PORT", 8000)
    return f"http://host.docker.internal:{port}/{path}"


def access() -> str:
    """Get the composer token."""
    if os.environ.get("CHAT_COMPOSER_ACCESS_TOKEN"):
        return os.environ["CHAT_COMPOSER_ACCESS_TOKEN"]

    raise ValueError(
        "CHAT_COMPOSER_ACCESS_TOKEN environment variable not set."
    )


def refresh() -> str:
    """Get the composer token."""
    if os.environ.get("CHAT_COMPOSER_REFRESH_TOKEN"):
        return os.environ["CHAT_COMPOSER_REFRESH_TOKEN"]

    raise ValueError(
        "CHAT_COMPOSER_REFRESH_TOKEN environment variable not set."
    )


def component_id() -> int:
    """Get the current component ID."""
    if _component_id is None:
        raise ValueError("component_id is None")

    return _component_id


def pipeline_id() -> int:
    """Get the current pipeline ID."""
    if _pipeline_id is None:
        raise ValueError("pipeline_id is None")

    return _pipeline_id


def component_state(id: Optional[int] = None) -> Dict[str, Any]:
    """Get the state of the component with the given ID."""
    if _states is None:
        raise ValueError("states is None")

    if id is None:
        id = component_id()

    for component_state in _states.component_states:
        if component_state.id == id:
            return component_state.state

    raise ValueError(f"component with id {id} not found")


def pipeline_state() -> Dict[str, Any]:
    """Get the state of the pipeline."""
    if _states is None:
        raise ValueError("states is None")

    return _states.pipeline_state


_pipeline_id: Optional[int] = None
_component_id: Optional[int] = None
_states: Optional[States] = None


class CurrentPipelineHelper:
    """Helper class for setting current pipeline."""

    def __init__(self, pipeline_id: int, user_message: str):
        """Initialize the helper"""
        self.pipeline_id = pipeline_id
        self.user_message = user_message
        self.response = None

    def __enter__(self):
        """Enter the context"""
        global _pipeline_id
        global _states

        response = requests.get(
            url(f"conductor/chat/states/{self.pipeline_id}/"),
            headers={"Authorization": f"Bearer {access()}"},
        )
        response.raise_for_status()

        _pipeline_id = self.pipeline_id
        _states = States(**response.json())

        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        exc_traceback: Optional[TracebackType],
    ):
        """Exit the context"""
        global _pipeline_id
        global _states

        try:
            # Save state if any
            if exc_type is None:
                response = requests.post(
                    url(f"conductor/chat/states/{self.pipeline_id}/"),
                    headers={"Authorization": f"Bearer {access()}"},
                    json=_states.model_dump(),
                )
                response.raise_for_status()

            # Save chat
            if exc_type is None:
                response = requests.patch(
                    url(f"conductor/chat/save/chat/{self.pipeline_id}/"),
                    headers={"Authorization": f"Bearer {access()}"},
                    json={
                        "user_message": self.user_message,
                        "resp_message": str(self.response),
                        "exit_code": 0,
                    },
                )
            else:
                traceback_str = "".join(traceback.format_exception(exc_value))
                response = requests.patch(
                    url(f"conductor/chat/save/chat/{self.pipeline_id}/"),
                    headers={"Authorization": f"Bearer {access()}"},
                    json={
                        "user_message": self.user_message,
                        "resp_message": (
                            # fmt: off
                            "Pipeline exited with code 1\n"
                            "```\n"
                            f"{traceback_str}"
                            "```"
                            # fmt: on
                        ),
                        "exit_code": 1,
                    },
                )
            response.raise_for_status()
        finally:
            _states = None
            _pipeline_id = None

        return True

    def set_response(self, response: Any):
        """Set the response"""
        self.response = response


class CurrentComponentHelper:
    """Helper class for setting current component."""

    def __init__(self, component_id: int):
        """Initialize the helper"""
        self.component_id = component_id

    def __enter__(self):
        """Enter the context"""
        global _component_id
        _component_id = self.component_id

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the context"""
        global _component_id
        _component_id = None


def init_pipeline(
    pipeline_id: int, user_message: str
) -> CurrentPipelineHelper:
    """Set the current pipeline"""
    return CurrentPipelineHelper(pipeline_id, user_message)


def init_component(
    component_id: int,
) -> CurrentComponentHelper:
    """Set the current component"""
    return CurrentComponentHelper(component_id)
