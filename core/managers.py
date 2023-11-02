from django.db import models


class ActivePipelineManager(models.Manager):
    """Manager for the active pipelines"""

    def get_queryset(self):
        """Return the active pipelines"""
        return super().get_queryset().filter(is_active=True)


class ActiveComponentInstanceManager(models.Manager):
    """Manager for the active component instnaces"""

    def get_queryset(self):
        """Return the active component instnaces"""
        return super().get_queryset().filter(is_active=True)
