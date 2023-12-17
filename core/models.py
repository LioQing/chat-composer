from __future__ import annotations

from typing import Dict, List

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import QuerySet

from utils.json_type import JsonType

from . import enums, managers, validators


class User(AbstractUser):
    """User model"""

    is_whitelisted = models.BooleanField(default=False)
    name = models.CharField(max_length=255)

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"

    def get_containment_name(self) -> str:
        """Get the name of the containment"""
        return f"chat-composer-containment-{self.username}"


class Component(models.Model):
    """Component model"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    function_name = models.CharField(
        max_length=255,
        validators=[validators.validate_function_name],
    )
    name = models.CharField(max_length=255, blank=True)
    arguments = models.JSONField(default=dict)
    return_type = models.CharField(
        max_length=255,
        choices=enums.ReturnType.choices(),
        default=enums.ReturnType.NONE,
    )
    description = models.TextField(default="", blank=True)
    code = models.TextField(blank=True)
    state = models.JSONField(default=dict)
    is_template = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_code(self) -> str:
        """Generate the code with the name"""
        return (
            # fmt: off
            f"def {self.function_name}():\n"
            "    \"\"\"Define your component here.\n"
            "\n"
            "    For more detailed documentation,\n"
            "    please click on the \"DOCS\" button\n"
            "    on the top right corner of the page.\n"
            "    \"\"\"\n"
            "    pass\n"
            # fmt: on
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

    def get_arguments(self) -> List[str]:
        """Get the arguments for this component.

        Returns:
            List[str]: Lines of codes for the arguments.
        """
        arguments: Dict[str, JsonType] = self.arguments
        lines = []
        for name in arguments:
            arg_lines = self.get_interpolatable_arguments(arguments[name])
            arg_lines[0] = f"{name}={arg_lines[0]}"
            arg_lines[-1] = f"{arg_lines[-1]},"
            lines.extend(arg_lines)

        return lines

    @staticmethod
    def get_interpolatable_arguments(value: Dict[str, JsonType]) -> List[str]:
        """Get the arguments for this component.

        If the argument is enabled, interpolated arguments will be
        returned, otherwise the default arguments will be returned.
        """
        if value["enabled"]:
            return [value["interpolated"]]

        return Component.get_json_arguments(value["default"])

    @staticmethod
    def get_json_arguments(value: JsonType) -> List[str]:
        """Get the arguments for this component.

        If the argument is enabled, interpolated arguments will be
        returned, otherwise the default arguments will be returned.
        """
        if isinstance(value, dict):
            lines = []
            for key in value:
                arg_lines = Component.get_interpolatable_arguments(value[key])
                arg_lines[0] = f"{repr(key)}: {arg_lines[0]}"
                arg_lines[-1] = f"{arg_lines[-1]},"
                lines.extend([f"    {l}" for l in arg_lines])

            return ["{"] + lines + ["}"]

        if isinstance(value, list):
            lines = []
            for item in value:
                arg_lines = Component.get_json_arguments(item)
                lines.extend([f"    {l}" for l in arg_lines])

            return ["["] + lines + ["]"]

        return [repr(value)]


class Pipeline(models.Model):
    """Pipeline model"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    response = models.TextField(default="", blank=True)
    state = models.JSONField(default=dict)
    description = models.TextField(default="", blank=True)
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

    def get_containment_directory(self) -> str:
        """Get the directory name containing this pipeline"""
        return f"{self.id}"


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
    user_message = models.TextField(blank=True)
    resp_message = models.TextField(blank=True)
    exit_code = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
