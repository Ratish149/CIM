# Generated by Django 5.0.4 on 2025-01-22 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('koshi_quality_standard', '0010_response_file_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
