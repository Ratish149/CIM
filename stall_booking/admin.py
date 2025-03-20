from django.contrib import admin
from .models import StallBooking,SponsorBooking,ThematicSession, ThematicRegistration, GuidedTour, SubSession, Panelist
from unfold.admin import ModelAdmin
from django.db import models
# Register your models here.

from tinymce.widgets import TinyMCE

class TinyMce(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }

class ThematicSessionAdmin(ModelAdmin):
    
    list_display = ('title', 'date', 'start_time', 'end_time')
    search_fields = ('title',)
    list_filter = ('date',)
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }

class SubSessionAdmin(ModelAdmin):
    
    list_display = ('title', 'thematic_session')
    search_fields = ('title', 'thematic_session__title')
    list_filter = ('thematic_session__title',)
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }

class PanelistAdmin(ModelAdmin):
    list_display = ('name', 'role', 'company','profile_image')
    search_fields = ('name', 'company')
    list_filter = ('role', 'thematic_session','sub_session')
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }

admin.site.register(StallBooking,ModelAdmin)
admin.site.register(SponsorBooking,ModelAdmin)
admin.site.register(ThematicSession, ThematicSessionAdmin)
admin.site.register(ThematicRegistration,ModelAdmin)
admin.site.register(GuidedTour,ModelAdmin)
admin.site.register(SubSession, SubSessionAdmin)
admin.site.register(Panelist, PanelistAdmin)
