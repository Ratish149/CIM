from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import IncubationCenter, RescheduleRequest

# Register your models here.


class RescheduleRequestInline(TabularInline):
    model = RescheduleRequest
    tab = True


@admin.register(IncubationCenter)
class IncubationCenterAdmin(ModelAdmin):
    inlines = (RescheduleRequestInline,)
    list_display = (
        "full_name",
        "email",
        "booking_date",
        "booking_type",
        "is_approved",
    )
    list_filter = (
        "booking_type",
        "is_approved",
    )
    search_fields = (
        "full_name",
        "email",
    )
    ordering = ("-booking_date",)
