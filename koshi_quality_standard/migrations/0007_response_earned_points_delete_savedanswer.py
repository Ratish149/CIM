# Generated by Django 5.1.4 on 2025-01-14 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('koshi_quality_standard', '0006_response_savedanswer'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='earned_points',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='SavedAnswer',
        ),
    ]
