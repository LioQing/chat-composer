# Generated by Django 4.2.5 on 2023-11-13 08:44

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='api_message',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='chat',
            name='user_message',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='component',
            name='function_name',
            field=models.CharField(max_length=255, validators=[core.validators.validate_function_name]),
        ),
        migrations.AlterField(
            model_name='component',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='pipeline',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]