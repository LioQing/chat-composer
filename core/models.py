from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models

from . import validators


class User(AbstractUser):
    """User model"""

    is_whitelisted = models.BooleanField(default=False)

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"


class Component(models.Model):
    """Component model"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(validators=[validators.validate_component_name])
    code = models.TextField()
    state = models.JSONField(default=dict)

    def generate_code(self) -> str:
        """Generate the code with the name"""
        return f"def {self.name}(user_message, data):\n    return data"

    def save(self, *args, **kwargs):
        """Save the component"""
        if not self.code:
            self.code = self.generate_code()
        super().save(*args, **kwargs)


class Pipeline(models.Model):
    """Pipeline model"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    components = models.ManyToManyField(Component, through="PipelineComponent")
    name = models.CharField()


class PipelineComponent(models.Model):
    """PipelineComponent model"""

    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
