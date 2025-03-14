from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE
from .models import BDSService,BDSCategory,Tags
from unfold.admin import ModelAdmin
# Register your models here.

class TinyMce(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE,},
    }
admin.site.register(BDSService,TinyMce)
admin.site.register(BDSCategory,ModelAdmin)
admin.site.register(Tags,ModelAdmin)

