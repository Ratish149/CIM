# Generated by Django 5.1.4 on 2025-01-20 17:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0004_remove_session_question_session_question'),
    ]

    operations = [
        migrations.RenameField(
            model_name='session',
            old_name='question',
            new_name='questions',
        ),
    ]