# Generated by Django 5.1.4 on 2024-12-24 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletter',
            name='subscribed',
            field=models.BooleanField(default=False),
        ),
    ]
