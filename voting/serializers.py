from rest_framework import serializers
from .models import Question, Voting

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'name', 'phone_number', 'question_text', 'vote_count', 'created_at']

class VotingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voting
        fields = ['id', 'question', 'name', 'phone_number', 'created_at']
