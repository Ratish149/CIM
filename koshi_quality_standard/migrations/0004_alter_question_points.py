# Generated by Django 5.1.4 on 2025-01-13 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('koshi_quality_standard', '0003_alter_question_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='points',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]