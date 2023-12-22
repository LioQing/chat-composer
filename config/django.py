from typing import List

from pydantic import Field

from . import BaseConfig


class DjangoConfig(BaseConfig):
    """Django config"""

    secret_key: str = Field()
    debug: bool = Field(False)
    allowed_hosts: List[str] = Field(["127.0.0.1", "localhost"])
    cors_allowed_origins: List[str] = Field([])
    time_zone: str = Field("UTC")
    admin_username: str = Field("admin")
    admin_password: str = Field("admin")
    admin_name: str = Field("Administrator")
    admin_email: str = Field("")
    admin_first_name: str = Field("")
    admin_last_name: str = Field("")

    class Config:
        env_prefix = "DJANGO_"
        env_file = ".env"


django_config = DjangoConfig()
