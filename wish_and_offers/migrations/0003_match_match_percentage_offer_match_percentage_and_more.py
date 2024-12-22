# Generated by Django 5.1.4 on 2024-12-22 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wish_and_offers', '0002_alter_match_offer_alter_match_wish_alter_offer_event_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='match_percentage',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='offer',
            name='match_percentage',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='wish',
            name='match_percentage',
            field=models.FloatField(default=0),
        ),
    ]
