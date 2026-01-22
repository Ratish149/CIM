import re
from datetime import datetime

from django.db import migrations, models


def clean_date_fields(apps, schema_editor):
    Event = apps.get_model("events", "Event")
    for event in Event.objects.all():
        changed = False
        for field in ["start_date", "end_date"]:
            val = getattr(event, field)
            if not val:
                continue

            str_val = str(val).strip()

            # Check if it's already in a valid format or close to it
            try:
                # If it matches YYYY-MM-DD, we are good
                datetime.strptime(str_val, "%Y-%m-%d")
                continue
            except ValueError:
                pass

            # Try to fix the specific format "13th Feb, 2026"
            try:
                # Remove ordinal suffixes st, nd, rd, th
                cleaned_val = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", str_val)
                parsed_date = datetime.strptime(cleaned_val, "%d %b, %Y").date()
                setattr(event, field, parsed_date)
                changed = True
            except ValueError:
                # If parsing fails, user requested to remove old data to avoid conflict
                setattr(event, field, None)
                changed = True
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
