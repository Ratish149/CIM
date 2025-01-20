# Generated by Django 5.1.4 on 2025-01-20 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mero_desh_merai_utpadan', '0016_alter_merodeshmeraiutpadan_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merodeshmeraiutpadan',
            name='status',
            field=models.CharField(choices=[('Rejected', 'Rejected'), ('Pending', 'Pending'), ('Approved', 'Approved')], default='Pending', max_length=255),
        ),
    ]
