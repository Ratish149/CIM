from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import (
    ApprenticeshipApplication,
    ApprenticeshipDocument,
    HireRequest,
    InternshipIndustry,
    JobApplication,
    JobPost,
    JobSeeker,
    Location,
    MajorGroup,
    MinorGroup,
    SavedJob,
    SubMajorGroup,
    UnitGroup,
)

admin.site.register(ApprenticeshipDocument, ModelAdmin)


@admin.register(ApprenticeshipApplication)
class ApprenticeshipApplicationAdmin(ModelAdmin):
    list_display = (
        "full_name",
        "mobile_number",
        "email_address",
        "district",
        "municipality",
        "ward",
        "created_at",
    )
    list_filter = ("district", "municipality", "ward", "created_at")
    search_fields = (
        "full_name",
        "mobile_number",
        "email_address",
        "district",
        "municipality",
        "ward",
    )
    date_hierarchy = "created_at"
    readonly_fields = ("created_at",)


@admin.register(MajorGroup)
class MajorGroupAdmin(ModelAdmin):
    list_display = ("code", "title")
    search_fields = ("code", "title")
    list_filter = ("code",)
    readonly_fields = ("slug",)

    fieldsets = ((None, {"fields": ("code", "title", "slug", "description")}),)


@admin.register(SubMajorGroup)
class SubMajorGroupAdmin(ModelAdmin):
    list_display = ("code", "title", "major_group")
    search_fields = ("code", "title", "major_group__title")
    list_filter = ("major_group",)
    readonly_fields = ("slug",)
    autocomplete_fields = ["major_group"]

    fieldsets = (
        (None, {"fields": ("code", "title", "major_group", "slug", "description")}),
    )


@admin.register(MinorGroup)
class MinorGroupAdmin(ModelAdmin):
    list_display = ("code", "title", "sub_major_group")
    search_fields = ("code", "title", "sub_major_group__title")
    list_filter = ("sub_major_group__major_group", "sub_major_group")
    readonly_fields = ("slug",)
    autocomplete_fields = ["sub_major_group"]

    fieldsets = (
        (None, {"fields": ("code", "title", "sub_major_group", "slug", "description")}),
    )


@admin.register(UnitGroup)
class UnitGroupAdmin(ModelAdmin):
    list_display = ("code", "title", "minor_group")
    search_fields = ("code", "title", "minor_group__title")
    list_filter = ("minor_group__sub_major_group__major_group", "minor_group")
    readonly_fields = ("slug",)
    autocomplete_fields = ["minor_group"]

    fieldsets = (
        (None, {"fields": ("code", "title", "minor_group", "slug", "description")}),
    )


@admin.register(InternshipIndustry)
class IndustryAdmin(ModelAdmin):
    list_display = ("name",)


@admin.register(JobPost)
class JobPostAdmin(ModelAdmin):
    list_display = (
        "title",
        "status",
        "employment_type",
        "required_skill_level",
        "posted_date",
        "deadline",
        "views_count",
        "applications_count",
    )
    list_filter = (
        "status",
        "employment_type",
        "required_skill_level",
        "required_education",
    )
    search_fields = ("title", "description")
    readonly_fields = ("slug", "posted_date", "views_count", "applications_count")
    autocomplete_fields = ["unit_group", "location"]
    date_hierarchy = "posted_date"
    list_editable = ["status"]

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "user",
                    "company_name",
                    "title",
                    "slug",
                    "unit_group",
                    "description",
                    "posted_date",
                    "status",
                )
            },
        ),
        (
            "Requirements",
            {
                "fields": (
                    "required_skill_level",
                    "required_education",
                    "responsibilities",
                    "requirements",
                )
            },
        ),
        (
            "Compensation & Location",
            {
                "fields": (
                    "show_salary",
                    "salary_range_min",
                    "salary_range_max",
                    "location",
                )
            },
        ),
        ("Job Details", {"fields": ("employment_type", "deadline")}),
        (
            "Statistics",
            {"fields": ("views_count", "applications_count"), "classes": ("collapse",)},
        ),
    )


@admin.register(JobApplication)
class JobApplicationAdmin(ModelAdmin):
    list_display = ("job", "applicant", "status", "applied_date", "updated_at")
    list_filter = ("status", "applied_date")
    search_fields = (
        "job__title",
        "applicant__user__username",
        "applicant__user__email",
    )
    date_hierarchy = "applied_date"
    readonly_fields = ("applied_date", "updated_at")
    autocomplete_fields = ["job", "applicant"]
    list_editable = ["status"]

    fieldsets = (
        (None, {"fields": ("job", "applicant", "status", "cover_letter")}),
        ("Dates", {"fields": ("applied_date", "updated_at")}),
    )


@admin.register(SavedJob)
class SavedJobAdmin(ModelAdmin):
    list_display = ("job", "job_seeker", "saved_date")
    list_filter = ("saved_date",)
    search_fields = (
        "job__title",
        "job_seeker__user__username",
        "job_seeker__user__email",
    )
    date_hierarchy = "saved_date"
    readonly_fields = ("saved_date",)
    autocomplete_fields = ["job", "job_seeker"]

    fieldsets = ((None, {"fields": ("job", "job_seeker", "saved_date")}),)


@admin.register(HireRequest)
class HireRequestAdmin(ModelAdmin):
    list_display = ("job", "job_seeker", "status", "requested_date")
    list_filter = ("status", "requested_date")
    search_fields = (
        "job__title",
        "job_seeker__user__username",
        "job_seeker__user__email",
    )
    date_hierarchy = "requested_date"
    readonly_fields = ("requested_date",)
    autocomplete_fields = ["job", "job_seeker"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "job",
                    "job_seeker",
                    "status",
                    "requested_date",
                    "message",
                    "seeker_message",
                )
            },
        ),
    )


@admin.register(JobSeeker)
class JobSeekerAdmin(ModelAdmin):
    list_display = (
        "user",
        "availability",
        "preferred_salary_range_from",
        "preferred_salary_range_to",
    )
    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
    )
    readonly_fields = ("slug",)


@admin.register(Location)
class LocationAdmin(ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    readonly_fields = ("slug",)
