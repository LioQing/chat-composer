from django.db import models


class GeminiProRequest(models.Model):
    """Gemini Pro request for Vertex AI API"""

    token_count = models.IntegerField()
    request = models.JSONField()
    response = models.JSONField()
    component = models.ForeignKey("core.Component", on_delete=models.CASCADE)
