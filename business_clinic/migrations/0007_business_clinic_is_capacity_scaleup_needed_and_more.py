# Generated by Django 5.1.4 on 2024-12-19 07:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business_clinic', '0006_alter_business_clinic_progress_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='business_clinic',
            name='is_capacity_scaleup_needed',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='business_clinic',
            name='is_common_issue',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='business_clinic',
            name='is_implementation_level',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='business_clinic',
            name='is_industry_specific',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='business_clinic',
            name='is_policy_level',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='business_clinic',
            name='is_procedural_hurdle',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='business_clinic',
            name='is_specific_policy_related',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='business_clinic',
            name='issue_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='business_clinic.issuecategory'),
        ),
        migrations.AlterField(
            model_name='business_clinic',
            name='issue_sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='business_clinic.issuesubcategory'),
        ),
        migrations.AlterField(
            model_name='business_clinic',
            name='progress_status',
            field=models.CharField(blank=True, choices=[('Issue Registere and documented', 'Issue Registere and documented'), ('Issue under desk study', 'Issue under desk study'), ('Issue forwarded to concern department', 'Issue forwarded to concern department'), ('Issue solve', 'Issue solve')], max_length=255, null=True),
        ),
    ]
