from django.contrib import admin
from .models import MeroDeshMeraiUtpadan,NatureOfIndustryCategory,NatureOfIndustrySubCategory
from unfold.admin import ModelAdmin

class MeroDeshMeraiUtpadanAdmin(ModelAdmin):
    list_display = (
        'name_of_company',
        'contact_name',
        'contact_number',
        'contact_email',
        'industry_size',
        'address_province',
        'address_district',
        'product_market',
        'created_at'
    )
    
    list_filter = (
        'industry_size',
        'product_market',
        'raw_material',
        'address_province',
        'member_of_cim',
        'interested_in_logo',
        'already_used_logo',
        'created_at'
    )
    
    search_fields = (
        'name_of_company',
        'contact_name',
        'contact_number',
        'contact_email',
        'address_province',
        'address_district',
        'address_municipality'
    )

# Register your models here.

admin.site.register(MeroDeshMeraiUtpadan, MeroDeshMeraiUtpadanAdmin)
admin.site.register(NatureOfIndustryCategory,ModelAdmin)
admin.site.register(NatureOfIndustrySubCategory,ModelAdmin)
