from rest_framework import serializers
from .models import Question, Answer, Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['document_name', 'points']

class QuestionSerializer(serializers.ModelSerializer):
    document=DocumentSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = ['id','question_text','category','document']

class AnswerSerializer(serializers.ModelSerializer):
    question_detail = QuestionSerializer(source='question', read_only=True)  # Add this for nested question details

    class Meta:
        model = Answer
        fields=['question', 'question_detail','document', 'is_true']