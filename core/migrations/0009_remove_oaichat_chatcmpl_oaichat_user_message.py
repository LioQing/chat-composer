# Generated by Django 4.2.5 on 2023-11-03 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_oaichat_chatcmpl_oaichat_pipeline'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='oaichat',
            name='chatcmpl',
        ),
        migrations.AddField(
            model_name='oaichat',
            name='user_message',
            field=models.CharField(default=''),
            preserve_default=False,
        ),
    ]
