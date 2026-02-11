from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import GraduateRoster, Institute

# Register your models here.


@admin.register(Institute)
class InstituteAdmin(ModelAdmin):
    list_display = (
        "institute_name",
        "email",
        "phone_number",
        "is_verified",
    )
    list_filter = ("is_verified",)
    search_fields = (
        "institute_name",
        "email",
        "phone_number",
        "address",
    )
    ordering = ("-created_at",)


@admin.register(GraduateRoster)
class GraduateRosterAdmin(ModelAdmin):
    list_display = (
        "institute",
        "name",
        "email",
        "phone_number",
    )
    list_filter = ("institute",)
    search_fields = (
        "institute__institute_name",
        "name",
        "email",
        "phone_number",
    )
    ordering = ("-created_at",)
