# Generated by Django 5.1.4 on 2025-01-21 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0006_alter_session_questions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='is_acepting_questions',
            field=models.BooleanField(default=False),
        ),
    ]
