from django.contrib import admin
from .models import InformationCategory, FAQ, Information, ContentItem
from unfold.admin import ModelAdmin

admin.site.register(InformationCategory, ModelAdmin)
admin.site.register(FAQ, ModelAdmin)
admin.site.register(Information, ModelAdmin)
admin.site.register(ContentItem, ModelAdmin)
