from django.contrib import admin
from .models import Question,Requirement,Response
from unfold.admin import ModelAdmin

# Register your models here.
class QuestionAdmin(ModelAdmin):
    list_display = ('text', 'points')
    search_fields = ('text',)
    list_filter = ('points',)

admin.site.register(Question,QuestionAdmin)
admin.site.register(Requirement,ModelAdmin)
admin.site.register(Response,ModelAdmin)
