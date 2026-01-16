from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe
from tinymce.widgets import TinyMCE
from unfold.admin import ModelAdmin, TabularInline

from .models import (
    AgendaItem,
    Attendee,
    Event,
    EventImage,
    EventOrganizer,
    Sponsor,
    Tag,
)

# Register your models here.


class EventImageInline(TabularInline):
    model = EventImage
    tab = True
    extra = 1
    readonly_fields = ["image_preview"]
    fields = ["image", "image_preview"]

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" width="150" height="auto" style="border-radius: 8px;" />'
            )
        return "No Image"

    image_preview.short_description = "Preview"


class EventAdmin(ModelAdmin):
    formfield_overrides = {models.TextField: {"widget": TinyMCE()}}
    list_display = (
        "title",
        "status",
        "order",
    )
    list_editable = ("order",)
    ordering = ("order",)
    inlines = [EventImageInline]


admin.site.register(Tag, ModelAdmin)
admin.site.register(EventOrganizer, ModelAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Attendee, ModelAdmin)
admin.site.register(AgendaItem, ModelAdmin)
admin.site.register(Sponsor, ModelAdmin)
