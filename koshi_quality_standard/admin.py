from django.contrib import admin
from .models import Question,Requirement,Response
from unfold.admin import ModelAdmin

# Register your models here.
admin.site.register(Question,ModelAdmin)
admin.site.register(Requirement,ModelAdmin)
admin.site.register(Response,ModelAdmin)
