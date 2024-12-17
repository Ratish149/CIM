from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Topic, TimeSlot, TrainingSession, Registration, Participant

admin.site.register(Topic,ModelAdmin)
admin.site.register(TimeSlot,ModelAdmin)
admin.site.register(TrainingSession,ModelAdmin)
admin.site.register(Registration,ModelAdmin)
admin.site.register(Participant,ModelAdmin)