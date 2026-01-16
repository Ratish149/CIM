from django.contrib import admin
from django.db import models
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
