# Generated by Django 5.1.4 on 2025-01-05 08:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business_clinic', '0010_remove_issue_issue_category_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='IssueAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_type', models.CharField(choices=[('status_change', 'Status Change'), ('comment', 'Comment'), ('assignment', 'Assignment')], max_length=50)),
                ('old_status', models.CharField(blank=True, max_length=50, null=True)),
                ('new_status', models.CharField(blank=True, max_length=50, null=True)),
                ('comment', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actions', to='business_clinic.issue')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
