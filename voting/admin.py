from django.contrib import admin
from .models import Question, Voting, Session, RunningSession
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

@admin.register(Session)
class SessionAdmin(ModelAdmin):
    list_display = ('title', 'is_acepting_questions')
    search_fields = ('title',)

@admin.register(RunningSession)
class RunningSessionAdmin(ModelAdmin):
    list_display = ('session',)
    search_fields = ('session__title',)
