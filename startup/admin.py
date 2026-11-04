from django.contrib import admin
from unfold.admin import ModelAdmin

from startup.models import StartUpRegistration


@admin.register(StartUpRegistration)
class StartUpRegistrationAdmin(ModelAdmin):
    list_display = (
        "id",
        "track",
        "full_name",
        "phone",
        "organization_name",
        "role",
        "status",
        "created_at",
    )
    list_filter = (
        "track",
        "status",
        "heard_about_us",
        "consent",
        "keep_updated",
    )
    search_fields = (
        "full_name",
        "phone",
        "email",
        "organization_name",
        "municipality",
        "notes",
    )
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 50

    fieldsets = (
        (
            "Enquiry Meta & Contact Information",
            {
                "fields": (
                    "track",
                    "status",
                    "full_name",
                    "phone",
                    "email",
                    "organization_name",
                    "role",
                    "municipality",
                    "notes",
                    "heard_about_us",
                    "consent",
                    "keep_updated",
                    "created_at",
                    "updated_at",
                )
            },
        ),
        (
            "Room 1 · Makerspace (Schools & Teachers) Details",
            {
                "classes": ("collapse",),
                "fields": (
                    "school_request",
                    "school_type",
                    "school_grades",
                    "school_students_count",
                    "school_teachers_count",
                    "school_preferred_date_1",
                    "school_preferred_date_2",
                    "school_session_slot",
                    "school_session_month",
                    "school_available_space",
                ),
            },
        ),
        (
            "Room 2 · Design Studio (College Students) Details",
            {
                "classes": ("collapse",),
                "fields": (
                    "college_programme",
                    "college_year",
                    "gender",
                    "age_group",
                    "idea_stage",
                    "interested_topics",
                    "preferred_contact_channel",
                    "willing_to_host_workshop",
                ),
            },
        ),
        (
            "Room 3 · Growth Room (Business Owners) Details",
            {
                "classes": ("collapse",),
                "fields": (
                    "district",
                    "business_registration_type",
                    "trading_duration",
                    "business_sector",
                    "employees_count",
                    "annual_turnover",
                    "ownership_diversity",
                    "area_of_interest",
                    "expo_visit_day",
                    "support_needs",
                    "biggest_challenge",
                ),
            },
        ),
    )
