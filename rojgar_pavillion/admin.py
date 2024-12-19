from django.contrib import admin
from unfold.admin import ModelAdmin,TabularInline
from .models import Topic, TimeSlot, Registration

admin.site.register(Topic, ModelAdmin)
admin.site.register(TimeSlot, ModelAdmin)
admin.site.register(Registration, ModelAdmin)