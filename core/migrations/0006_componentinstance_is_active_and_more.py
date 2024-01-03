# Generated by Django 4.2.5 on 2023-11-02 18:56

import core.models
from django.db import migrations, models


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


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_componentinstance_remove_pipeline_components_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='componentinstance',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='component',
            name='description',
            field=models.JSONField(default=component_description_default),
        ),
    ]
