from django.contrib import admin
from .models import Question, Answer, Document
from unfold.admin import ModelAdmin

# Register your models here.

admin.site.register(Question,ModelAdmin)
admin.site.register(Answer,ModelAdmin)
admin.site.register(Document,ModelAdmin)
