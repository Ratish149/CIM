from rest_framework import serializers
from .models import Question,Requirement


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'points']

class RequirementSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Requirement
        fields = ['id', 'name', 'questions']

class AnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()  # Ensure question_id is an integer
    answer = serializers.BooleanField()       # Ensure answer is a boolean

class RequirementAnswerSerializer(serializers.Serializer):
    requirement_id = serializers.IntegerField()
    is_relevant = serializers.BooleanField()
    answers = serializers.ListField(
        child=AnswerSerializer(),  # Use the corrected AnswerSerializer here
        required=False
    )

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()