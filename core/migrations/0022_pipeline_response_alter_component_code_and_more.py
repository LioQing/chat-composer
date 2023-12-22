# Generated by Django 4.2.5 on 2023-12-09 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_alter_component_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pipeline',
            name='response',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='component',
            name='code',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='component',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='pipeline',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]