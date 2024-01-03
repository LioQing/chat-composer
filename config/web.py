from pydantic import Field

from . import BaseConfig


class WebConfig(BaseConfig):
    """Web configuration"""

    url: str = Field(default="http://localhost")
    port: int = Field(default=8000)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "WEB_"


web_config = WebConfig()
