from django.core.management.base import BaseCommand

from core import models


class Command(BaseCommand):
    """Initialize component templates."""

    help = "Initialize component templates."

    def handle(self, *args, **options):
        """Initialize component templates."""
        additional = {"user_id": 1}

        for template in TEMPLATES:
            models.Component.objects.filter(
                name=template["name"], is_template=True
            ).delete()

            models.Component.objects.update_or_create(
                defaults=template | additional,
            )


# fmt: off
TEMPLATES = [
    {
        "name": "Empty Template",
        "function_name": "empty_template",
        "description": {
            "type": "doc",
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": "This is an empty template, but it will get you started."
                        }
                    ]
                },
                {
                    "type": "paragraph"
                },
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": "In a component, you can do the following:"
                        }
                    ]
                },
                {
                    "type": "bulletList",
                    "content": [
                        {
                            "type": "listItem",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [
                                        {
                                            "type": "text",
                                            "text": "Click on any empty area on the component to edit its attributes."
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "type": "listItem",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [
                                        {
                                            "type": "text",
                                            "text": "Click on the checkbox on the left to toggle enable or disable it."
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "type": "listItem",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [
                                        {
                                            "type": "text",
                                            "text": "Click on the code icon on the right to code the logics."
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "type": "listItem",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [
                                        {
                                            "type": "text",
                                            "text": "Click on the rubbish bin icon on the right to delete the component."
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "type": "paragraph"
                },
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": "The function name specified in the attribute must match the function you defined in the code logic. The function should have the following signature:"
                        }
                    ]
                },
                {
                    "type": "paragraph"
                },
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": "Arguments:"
                        }
                    ]
                },
                {
                    "type": "bulletList",
                    "content": [
                        {
                            "type": "listItem",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [
                                        {
                                            "type": "text",
                                            "marks": [
                                                {
                                                    "type": "code"
                                                }
                                            ],
                                            "text": "user_message"
                                        },
                                        {
                                            "type": "text",
                                            "text": " (str): The mesasge user entered in the chatbox."
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "type": "listItem",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [
                                        {
                                            "type": "text",
                                            "marks": [
                                                {
                                                    "type": "code"
                                                }
                                            ],
                                            "text": "data"
                                        },
                                        {
                                            "type": "text",
                                            "text": " (Dict[str, Any]): The data previous component passed to here."
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "type": "paragraph"
                },
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": "Returns:"
                        }
                    ]
                },
                {
                    "type": "bulletList",
                    "content": [
                        {
                            "type": "listItem",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [
                                        {
                                            "type": "text",
                                            "marks": [
                                                {
                                                    "type": "code"
                                                }
                                            ],
                                            "text": "data"
                                        },
                                        {
                                            "type": "text",
                                            "text": " (Dict[str, Any]): The data to be passed to the next component."
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "type": "paragraph"
                },
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": "The function may also have access to the following global variables for persistent data storage or configuration:"
                        }
                    ]
                },
                {
                    "type": "bulletList",
                    "content": [
                        {
                            "type": "listItem",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [
                                        {
                                            "type": "text",
                                            "marks": [
                                                {
                                                    "type": "code"
                                                }
                                            ],
                                            "text": "state"
                                        },
                                        {
                                            "type": "text",
                                            "text": " (Dict[str, Any]): The state of the component."
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "type": "listItem",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [
                                        {
                                            "type": "text",
                                            "marks": [
                                                {
                                                    "type": "code"
                                                }
                                            ],
                                            "text": "pstate"
                                        },
                                        {
                                            "type": "text",
                                            "text": " (Dict[str, Any]): The state of the pipeline."
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "type": "paragraph"
                },
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": "For more detailed documentation, please click on the \"DOCS\" button on the top right corner of the page."
                        }
                    ]
                }
            ]
        },
        "code": "\
from typing import Dict, Any\n\
\n\
def empty_template(user_message: str, data: Dict[str, Any]) -> Dict[str, Any]:\n\
    return data\n\
        ",
        "state": {},
        "is_template": True
    }
]
# fmt: on
