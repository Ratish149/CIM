from django.contrib import admin
from unfold.admin import ModelAdmin
from django.db import models
from tinymce.widgets import TinyMCE
from .models import BusinessInformation,BusinessCategory
# Register your models here.

class TinyMce(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE,},
    }
admin.site.register(BusinessInformation,TinyMce)
admin.site.register(BusinessCategory,ModelAdmin)
