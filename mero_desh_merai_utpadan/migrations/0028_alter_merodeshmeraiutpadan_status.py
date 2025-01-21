# Generated by Django 5.1.4 on 2025-01-21 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mero_desh_merai_utpadan', '0027_alter_merodeshmeraiutpadan_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merodeshmeraiutpadan',
            name='status',
            field=models.CharField(choices=[('Approved', 'Approved'), ('Pending', 'Pending'), ('Rejected', 'Rejected')], default='Pending', max_length=255),
        ),
    ]
