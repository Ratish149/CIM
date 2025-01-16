# Generated by Django 5.1.4 on 2025-01-16 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('koshi_quality_standard', '0008_alter_question_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='category',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='response',
            name='percentage',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
