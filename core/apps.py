from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        """Run when the app is ready"""
        from engine.containment import containment

        containment.create_user_containers()
