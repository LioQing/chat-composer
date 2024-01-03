from pydantic import Field

from . import BaseConfig


class ContainmentConfig(BaseConfig):
    """Containment config"""

    image: str = Field("python:3.11.5-slim")
    base_directory: str = Field("/composer")
    python_venv: str = Field(".venv")

    class Config:
        env_prefix = "CONTAINMENT_"
        env_file = ".env"


containment_config = ContainmentConfig()
