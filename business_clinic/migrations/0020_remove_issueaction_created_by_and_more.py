# Generated by Django 5.1.4 on 2025-01-13 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business_clinic', '0019_alter_issueaction_action_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issueaction',
            name='created_by',
        ),
        migrations.AlterField(
            model_name='issueaction',
            name='action_type',
            field=models.CharField(choices=[('status_change', 'Status Change'), ('implementation_level_change', 'Implementation Level Change'), ('industry_category_change', 'Industry Category Change'), ('industry_subcategory_change', 'Industry Subcategory Change'), ('nature_of_issue_change', 'Nature of Issue Change'), ('industry_size_change', 'Industry Size Change'), ('industry_specific_or_common_issue_change', 'Industry Specific or Common Issue Change'), ('policy_related_or_procedural_issue_change', 'Policy Related or Procedural Issue Change')], max_length=50),
        ),
    ]
