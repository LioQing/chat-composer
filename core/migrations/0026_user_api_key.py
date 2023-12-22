# Generated by Django 4.2.5 on 2023-12-17 06:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rest_framework_api_key', '0005_auto_20220110_1102'),
        ('core', '0025_chat_exit_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='api_key',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to='rest_framework_api_key.apikey'),
        ),
    ]