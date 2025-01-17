from rest_framework import serializers
from .models import Question, Voting, Session, RunningSession

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'name', 'phone_number', 'question_text', 'vote_count', 'created_at']

class VotingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voting
        fields = ['id', 'question', 'name', 'phone_number', 'created_at']

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'title', 'questions', 'is_acepting_questions']

class SessionOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'title', 'is_acepting_questions']

class RunningSessionSerializer(serializers.ModelSerializer):
    session=SessionOnlySerializer()
    class Meta:
        model = RunningSession
        fields = ['id', 'session']
