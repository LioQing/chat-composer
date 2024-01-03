from . import BaseConfig


class VertexAiConfig(BaseConfig):
    """Configurations for Vertex AI API"""

    project_id: str
    location: str
    api_key: str

    class Config:
        env_prefix = "VERTEXAI_"
        env_file = ".env"


vertexai_config = VertexAiConfig()
