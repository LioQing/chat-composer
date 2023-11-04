# Generated by Django 4.2.5 on 2023-11-03 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_componentinstance_is_active_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OaiChat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_message', models.CharField()),
                ('is_first', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
