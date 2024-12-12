from django.contrib import admin
from .models import IssueCategory,NatureOfIndustryCategory,IssueSubCategory,NatureOfIndustrySubCategory,NatureOfIndustrySubSubCategory,Business_Clinic
from unfold.admin import ModelAdmin
# Register your models here.
admin.site.register(IssueCategory,ModelAdmin)
admin.site.register(NatureOfIndustryCategory,ModelAdmin)    
admin.site.register(IssueSubCategory,ModelAdmin)
admin.site.register(NatureOfIndustrySubCategory,ModelAdmin)
admin.site.register(NatureOfIndustrySubSubCategory,ModelAdmin)
admin.site.register(Business_Clinic,ModelAdmin)
