from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import QuerySet

from . import managers, validators


class User(AbstractUser):
    """User model"""

    is_whitelisted = models.BooleanField(default=False)
    name = models.CharField(max_length=255)

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"


class Component(models.Model):
    """Component model"""

    def component_description_default():
        """Default description for a component"""
        return {
            "type": "doc",
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": "Description",
                        },
                    ],
                },
            ],
        }

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    function_name = models.CharField(
        max_length=255, validators=[validators.validate_function_name]
    )
    description = models.JSONField(default=component_description_default)
    code = models.TextField()
    state = models.JSONField(default=dict)
    is_template = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_code(self) -> str:
        """Generate the code with the name"""
        return (
            f"def {self.function_name}(user_message, data):\n    return data"
        )

    def save(self, *args, **kwargs):
        """Save the component"""
        if not self.code:
            self.code = self.generate_code()
        super().save(*args, **kwargs)

    def get_pipeline(self) -> Pipeline:
        """Get the pipelines for this component"""
        instance: ComponentInstance = self.componentinstance
        return instance.pipeline


class Pipeline(models.Model):
    """Pipeline model"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    state = models.JSONField(default=dict)
    is_safe = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = managers.ActivePipelineManager()
    all_objects = models.Manager()

    def save(self, *args, **kwargs):
        """Save the pipeline"""
        if not self.name:
            self.name = f"Pipeline {self.user.pipeline_set.count() + 1}"
        super().save(*args, **kwargs)

    def get_components(self) -> QuerySet[Component]:
        """Get the components for this pipeline"""
        instances: QuerySet[ComponentInstance] = self.componentinstance_set
        return Component.objects.filter(
            id__in=instances.filter(is_enabled=True).values_list(
                "component_id", flat=True
            )
        ).order_by("componentinstance__order")


class ComponentInstance(models.Model):
    """ComponentInstance model"""

    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE)
    component = models.OneToOneField(Component, on_delete=models.CASCADE)
    is_enabled = models.BooleanField(default=True)
    order = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    objects = managers.ActiveComponentInstanceManager()
    all_objects = models.Manager()


class Chat(models.Model):
    """Chat model"""

    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE)
    user_message = models.TextField()
    api_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
