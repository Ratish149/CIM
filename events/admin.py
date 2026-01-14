from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE
from unfold.admin import ModelAdmin

from .models import AgendaItem, Attendee, Event, EventOrganizer, Sponsor, Tag


# Register your models here.
class EventAdmin(ModelAdmin):
    formfield_overrides = {models.TextField: {"widget": TinyMCE()}}
    list_display = (
        "title",
        "status",
        "order",
    )
    list_editable = ("order",)
    ordering = ("order",)


admin.site.register(Tag, ModelAdmin)
admin.site.register(EventOrganizer, ModelAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Attendee, ModelAdmin)
admin.site.register(AgendaItem, ModelAdmin)
admin.site.register(Sponsor, ModelAdmin)
