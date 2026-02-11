from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import ExperienceZoneBooking


@admin.register(ExperienceZoneBooking)
class ExperienceZoneBookingAdmin(ModelAdmin):
    list_display = (
        "company_name",
        "preferred_month",
        "subcategory",
        "status",
        "created_at",
    )
    list_filter = ("status", "preferred_month", "subcategory")
    search_fields = ("company_name", "email", "contact_person")
