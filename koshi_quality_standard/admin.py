from django.contrib import admin
from .models import Question,Requirement
from unfold.admin import ModelAdmin

# Register your models here.
admin.site.register(Question,ModelAdmin)
admin.site.register(Requirement,ModelAdmin)
