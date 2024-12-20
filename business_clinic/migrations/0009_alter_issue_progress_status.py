# Generated by Django 5.1.4 on 2024-12-20 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business_clinic', '0008_rename_business_clinic_issue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='progress_status',
            field=models.CharField(blank=True, choices=[('Issue Registere and documented', 'Issue Registere and documented'), ('Issue under desk study', 'Issue under desk study'), ('Issue forwarded to concern department', 'Issue forwarded to concern department'), ('Issue solve', 'Issue solve'), ('Issue rejected', 'Issue rejected')], max_length=255, null=True),
        ),
    ]