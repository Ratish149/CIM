from django.contrib import admin
from .models import NatureOfIndustryCategory, NatureOfIndustrySubCategory, Issue, IssueAction
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
        'share_contact_details',
        'forward_to_authority',
        'implementation_level',
    ]
    list_filter = [
        'progress_status',
        'share_contact_details',
        'forward_to_authority',
        'implementation_level',
        'industry_specific_or_common_issue',
        'policy_related_or_procedural_issue',
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
                'implementation_level'
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

@admin.register(IssueAction)
class IssueActionAdmin(ModelAdmin):
    list_display = [
        'issue',
        'action_type',
        'get_change_details',
        'created_at',
    ]
    list_filter = [
        'action_type',
        'created_at',
    ]
    search_fields = [
        'issue__title',
        'comment',
        'old_value',
        'new_value'
    ]
    readonly_fields = ['created_at']

    def get_change_details(self, obj):
        if obj.action_type == 'status_change':
            return f"From {obj.old_status} to {obj.new_status}"
        elif obj.action_type in [
            'implementation_level_change',
            'share_contact_change',
            'forward_authority_change',
            'industry_category_change',
            'industry_subcategory_change',
            'nature_of_issue_change',
            'industry_size_change',
            'industry_specific_or_common_issue_change',
            'policy_related_or_procedural_issue_change'
        ]:
            return f"From {obj.old_value} to {obj.new_value}"
        return obj.comment
    get_change_details.short_description = 'Change Details'
