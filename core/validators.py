from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_function_name(value: str):
    """Validate component name"""
    if not value.isidentifier():
        raise ValidationError(
            _(
                "Component name must be a valid Python identifier. "
                "See https://docs.python.org/3/reference/lexical_analysis.html"
                "#identifiers"
            )
        )
