from django.contrib import admin
from .models import Contact, Newsletter
from unfold.admin import ModelAdmin
# Register your models here.
admin.site.register(Contact,ModelAdmin)
admin.site.register(Newsletter,ModelAdmin)
