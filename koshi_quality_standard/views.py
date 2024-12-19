from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import Question, Document,Answer, SavedAnswer
from .serializers import QuestionSerializer, AnswerSerializer, SavedAnswerSerializer

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

        saved_answers = SavedAnswer.objects.create(total_score=0)  # We'll update the score later


        for answer_data in answers_data:
            question_id = answer_data.get('question')
            document_id = answer_data.get('document')
            is_true = answer_data.get('is_true', False)

            question = Question.objects.get(id=question_id)
            document = Document.objects.get(id=document_id)

            # # Create and save the answer
            # Answer.objects.create(
            #     question=question,
            #     document=document,
            #     is_true=is_true
            # )
            # Calculate score
            if is_true:
                total_score += document.points
        
        saved_answers.total_score = total_score
        saved_answers.save()

        # Serialize the saved answers
        # serializer = self.get_serializer(saved_answers, many=True)
        saved_serializer=SavedAnswerSerializer(saved_answers)

        return Response({
            'saved_answers': saved_serializer.data
        })
        # return Response({
        #     'total_score': total_score,
        #     'answers': serializer.data
        # })
