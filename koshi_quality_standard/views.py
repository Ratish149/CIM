from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import Question, Document,Answer
from .serializers import QuestionSerializer, AnswerSerializer

# Create your views here.

class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class AnswerListCreateView(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def create(self, request, *args, **kwargs):
        answers_data = request.data.get('answers', [])
        total_score = 0

        for answer_data in answers_data:
            question_id = answer_data.get('question')
            document_id = answer_data.get('document')
            is_true = answer_data.get('is_true', False)

            question = Question.objects.get(id=question_id)
            document = Document.objects.get(id=document_id)

            # Calculate score
            if is_true:
                total_score += document.points
                print (f'totalscore: {total_score}')

        return Response({
            'total_score': total_score,
        })
