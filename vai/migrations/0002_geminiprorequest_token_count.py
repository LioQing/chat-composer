# Generated by Django 4.2.5 on 2024-01-06 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vai', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='geminiprorequest',
            name='token_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
