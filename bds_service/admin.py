from django.contrib import admin
from .models import BDSService,BDSCategory,Tags
from unfold.admin import ModelAdmin
# Register your models here.

admin.site.register(BDSService,ModelAdmin)
admin.site.register(BDSCategory,ModelAdmin)
admin.site.register(Tags,ModelAdmin)

