from django.contrib import admin
from .models import Question, Voting
from unfold.admin import ModelAdmin

# Register your models here.
@admin.register(Question)
class QuestionAdmin(ModelAdmin):
    list_display = ('name', 'phone_number', 'vote_count', 'created_at')
    search_fields = ('name', 'question_text')

@admin.register(Voting)
class VotingAdmin(ModelAdmin):
    list_display = ('name', 'phone_number', 'question', 'created_at')
    search_fields = ('name', 'question__name')
