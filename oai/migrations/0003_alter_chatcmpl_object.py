# Generated by Django 4.2.5 on 2023-11-13 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oai', '0002_alter_chatcmpl_object_alter_functioncall_arguments_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatcmpl',
            name='object',
            field=models.CharField(),
        ),
    ]
