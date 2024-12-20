from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import CustomUser, Organization, File

class FileInline(admin.TabularInline):
    model = File
    extra = 1

class CustomUserAdmin(ModelAdmin):
   list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active')
   search_fields = ('email', 'username', 'first_name', 'last_name')
   list_filter = ('is_staff', 'is_active')
   ordering = ('email',)
   
class OrganizationAdmin(ModelAdmin):
   list_display = ('name', 'email', 'phone_number', 'address', 'website')
   search_fields = ('name', 'email', 'phone_number', 'address', 'website')
   list_filter = ('name', 'email', 'phone_number', 'address', 'website')
   ordering = ('name',)
   inlines = [FileInline]

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Organization, OrganizationAdmin)