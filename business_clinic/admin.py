from django.contrib import admin
from .models import NatureOfIndustryCategory, NatureOfIndustrySubCategory, Issue
from unfold.admin import ModelAdmin

@admin.register(NatureOfIndustryCategory)
class NatureOfIndustryCategoryAdmin(ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(NatureOfIndustrySubCategory)
class NatureOfIndustrySubCategoryAdmin(ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']
    search_fields = ['name', 'category__name']

@admin.register(Issue)
class IssueAdmin(ModelAdmin):
    list_display = [
        'title', 
        'name_of_company',
        'nature_of_issue',
        'industry_size',
        'progress_status',
        'created_at'
    ]
    list_filter = [
        'nature_of_issue',
        'industry_size',
        'progress_status',
        'member_of_CIM',
        'industry_specific_or_common_issue',
        'policy_related_or_procedural_issue',
        'implementation_level_policy_level_or_capacity_scale'
    ]
    search_fields = [
        'title',
        'name_of_company',
        'contact_name',
        'contact_email'
    ]
    fieldsets = (
        ('Issue Details', {
            'fields': ('title', 'description', 'issue_image')
        }),
        ('Categorization', {
            'fields': (
                'nature_of_issue',
                'industry_specific_or_common_issue',
                'policy_related_or_procedural_issue',
                'implementation_level_policy_level_or_capacity_scale'
            )
        }),
        ('Industry Information', {
            'fields': (
                'industry_size',
                'nature_of_industry_category',
                'nature_of_industry_sub_category'
            )
        }),
        ('Company Information', {
            'fields': ('name_of_company', 'member_of_CIM')
        }),
        ('Address Information', {
            'fields': (
                'address_province',
                'address_district',
                'address_municipality',
                'address_ward',
                'address_street'
            )
        }),
        ('Contact Information', {
            'fields': (
                'contact_name',
                'contact_designation',
                'contact_number',
                'contact_alternate_number',
                'contact_email'
            )
        }),
        ('Status', {
            'fields': ('progress_status',)
        })
    )
