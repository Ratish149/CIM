import re
from datetime import datetime

from django.db import migrations, models


def clean_date_fields(apps, schema_editor):
    Event = apps.get_model("events", "Event")
    for event in Event.objects.all():
        changed = False
        for field in ["start_date", "end_date"]:
            val = getattr(event, field)
            if val:
                # Remove ordinal suffixes st, nd, rd, th
                cleaned_val = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", str(val))
                try:
                    parsed_date = datetime.strptime(cleaned_val, "%d %b, %Y").date()
                    setattr(event, field, parsed_date)
                    changed = True
                except ValueError:
                    # If it's already in YYYY-MM-DD or doesn't match, leave it
                    # PostgreSQL might still fail if it's garbage, but this fixes the known issue
                    pass
        if changed:
            event.save()


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0021_alter_eventimage_image"),
    ]

    operations = [
        migrations.RunPython(clean_date_fields),
        migrations.AlterField(
            model_name="event",
            name="end_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="event",
            name="start_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
