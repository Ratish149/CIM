from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import LearnAndWorkBooking


@admin.register(LearnAndWorkBooking)
class LearnAndWorkBookingAdmin(ModelAdmin):
    list_display = [
        "zone", "date", "time", "school", "grade",
        "teacher", "phone", "students", "created_at",
    ]
    list_filter = ["zone", "date", "time"]
    search_fields = ["school", "teacher", "phone", "email"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
