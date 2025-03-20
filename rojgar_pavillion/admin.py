from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Topic, TimeSlot, Registration

class RegistrationAdmin(ModelAdmin):
    list_display = ('first_name','time_slot', 'registration_type', 'total_participants', 'total_price', 'created_at')
    list_filter = ('registration_type', 'created_at', 'time_slot')

admin.site.register(Topic, ModelAdmin)
admin.site.register(TimeSlot, ModelAdmin)
admin.site.register(Registration, RegistrationAdmin)