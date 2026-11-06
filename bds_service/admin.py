from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE
from unfold.admin import ModelAdmin

from .models import BDSCategory, BDSConnect, BDSService, Tags

# Register your models here.


class TinyMce(ModelAdmin):
    formfield_overrides = {
        models.TextField: {
            "widget": TinyMCE,
        },
    }


@admin.register(BDSConnect)
class BDSConnectAdmin(ModelAdmin):
    list_display = [
        "name",
        "track",
        "phone",
        "email",
        "business_name",
        "district",
        "created_at",
    ]
    list_filter = ["track", "district", "sector", "registered", "created_at"]
    search_fields = ["name", "phone", "email", "business_name"]
    readonly_fields = ["created_at"]
    ordering = ["-created_at"]


admin.site.register(BDSService, TinyMce)
admin.site.register(BDSCategory, ModelAdmin)
admin.site.register(Tags, ModelAdmin)
