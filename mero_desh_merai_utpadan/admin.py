from django.contrib import admin
from .models import MeroDeshMeraiUtpadan,NatureOfIndustryCategory,NatureOfIndustrySubCategory,NatureOfIndustrySubSubCategory
from unfold.admin import ModelAdmin
# Register your models here.

admin.site.register(MeroDeshMeraiUtpadan,ModelAdmin)
admin.site.register(NatureOfIndustryCategory,ModelAdmin)
admin.site.register(NatureOfIndustrySubCategory,ModelAdmin)
admin.site.register(NatureOfIndustrySubSubCategory,ModelAdmin)