# Generated by Django 5.1.4 on 2025-01-07 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business_registration', '0002_contentitem_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentitem',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='faq',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='information',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='informationcategory',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]
