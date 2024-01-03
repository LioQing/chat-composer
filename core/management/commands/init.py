from django.core.management.base import BaseCommand

from config.django import django_config
from core import models

PIPELINE_TEMPLATES = [
    {
        "name": "Default",
        "response": "default.ret",
        "state": {},
        "description": (
            "# Getting Started\n\n## Pipeline\n\nPipeline is a sequence of"
            " components chained together.\n\nThe components of a pipeline are"
            " called in the order they are shown.\n\nComponents must have"
            " distinct function name (but not name).\n\nDisabled components"
            " will not run.\n\n## Interpolated\n\nIn any text field with a"
            ' placeholder "Interpolated", you can enter the input in'
            ' Python.\n\nFor example, you can enter `"Hello World"` (with the'
            " quotations) to get a string.\n\n## Components\n\nYou can also"
            " access each component's arguments and return value with the"
            " member `arg` (which is a dictionary) and `ret`"
            " respectively.\n\nFor example, in the response of the pipeline"
            " attributes, you can enter `default.ret` to get the return value"
            ' of the "Default" component for the response.\n\n## More\n\nClick'
            ' the "DOCS" button on the top right to see more.'
        ),
        "is_active": True,
    }
]


COMPONENT_TEMPLATES = [
    {
        "function_name": "default",
        "name": "Default",
        "arguments": {
            "user_message": {
                "default": "",
                "enabled": True,
                "interpolated": "user_message",
            }
        },
        "return_type": "string",
        "description": (
            "# Getting Started\n\n## Components\n\nComponents are codes which"
            " stores the logic of the code.\n\nYou can specify the name,"
            " function name, return type, parameters and arguments of the"
            " component.\n\nFunction name must be distinct within a pipeline,"
            " so remember to change the function name after adding it!\n\n##"
            " Interpolated\n\nIn any text field with a placeholder"
            ' "Interpolated", you can enter the input in Python.\n\nFor'
            ' example, you can enter `"Hello World"` (with the quotations) to'
            " get a string.\n\n## States\n\nYou can access states of the"
            " pipeline and component, which are persistent data stored in the"
            " backend for the pipeline and component.\n\nYou may access the"
            " states using the Composer module via the functions"
            " `pipeline_state` and `component_state` respectively.\n\n##"
            ' More\n\nClick the "DOCS" button on the top right to see more.'
        ),
        "code": (
            "from modules import composer\n\ndef default(user_message: str) ->"
            " str:\n    state: dict = composer.component_state()\n   "
            ' state["counter"] += 1\n    return f"Your message was:'
            " {user_message} (counter: {state['counter']})\""
        ),
        "state": {"counter": 0},
        "is_template": True,
    },
    {
        "function_name": "oai_chatcmpl",
        "name": "OpenAI Chat Completion",
        "arguments": {
            "user_message": {
                "default": "",
                "enabled": True,
                "interpolated": "user_message",
            }
        },
        "return_type": "string",
        "description": (
            "# OpenAI Chat Completion\n\nThis is a simple example of the OAI"
            " module.\n\nIt calls the OpenAI chat completion for answering"
            ' user questions.\n\n## More\n\nClick the "DOCS" button on the top'
            " right to see more."
        ),
        "code": (
            "from modules import oai\n\ndef oai_chatcmpl(user_message: str) ->"
            " str:\n    response ="
            " oai.api.chatcmpl(oai.models.ChatcmplRequest(\n       "
            " messages=[\n            oai.models.Message(\n               "
            ' role=oai.enums.Role.SYSTEM,\n                content="You are an'
            " assistant to answer user's question.\",\n            ),\n       "
            "     oai.models.Message(\n               "
            " role=oai.enums.Role.USER,\n               "
            " content=user_message,\n            ),\n        ]\n    ))\n\n   "
            " return response.choices[0].message.content"
        ),
        "state": {},
        "is_template": True,
    },
    {
        "function_name": "google_gemini_pro",
        "name": "Google Gemini Pro",
        "arguments": {
            "user_message": {
                "default": "",
                "enabled": True,
                "interpolated": "user_message",
            }
        },
        "return_type": "string",
        "description": (
            "# Google Gemini Pro\n\nThis is a simple example of the VAI"
            " module.\n\nIt calls Google's Gemini API for answering user's"
            " question.\n\nVAI stands for Vertex AI, which is one of Google"
            ' Cloud\'s services.\n\n## More\n\nClick the "DOCS" button on the'
            " top right to see more."
        ),
        "code": (
            "from modules import vai\n\ndef google_gemini_pro(user_message:"
            " str) -> str:\n    response ="
            " vai.api.gemini_pro(vai.models.GeminiRequest(\n       "
            " contents=user_message\n    ))\n\n    return response.text"
        ),
        "state": {},
        "is_template": True,
    },
]


class Command(BaseCommand):
    """Initialize everything."""

    help = "Initialize everything."

    def handle(self, *args, **options):
        """Initialize everything."""
        # Create admin if there is no superuser
        if models.User.objects.filter(is_superuser=True).exists():
            return

        admin: models.User = models.User.objects.create_superuser(
            username=django_config.admin_username,
            password=django_config.admin_password,
            name=django_config.admin_name,
            email=django_config.admin_email,
            first_name=django_config.admin_first_name,
            last_name=django_config.admin_last_name,
            is_whitelisted=True,
        )
        admin.save()

        # Create pipeline templates
        for pipeline_template in PIPELINE_TEMPLATES:
            models.Pipeline.objects.create(**pipeline_template, user=admin)

        # Create component templates
        for component_template in COMPONENT_TEMPLATES:
            models.Component.objects.create(**component_template, user=admin)
