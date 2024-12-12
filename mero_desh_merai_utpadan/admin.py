from django.contrib import admin
from .models import MeroDeshMeraiUtpadan,NatureOfIndustryCategory,NatureOfIndustrySubCategory
from unfold.admin import ModelAdmin
# Register your models here.

admin.site.register(MeroDeshMeraiUtpadan,ModelAdmin)
admin.site.register(NatureOfIndustryCategory,ModelAdmin)
admin.site.register(NatureOfIndustrySubCategory,ModelAdmin)
