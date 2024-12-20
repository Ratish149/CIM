from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Event, Attendee,AgendaItem,Tag
# Register your models here.
admin.site.register(Tag,ModelAdmin)
admin.site.register(Event,ModelAdmin)
admin.site.register(Attendee,ModelAdmin)
admin.site.register(AgendaItem,ModelAdmin)