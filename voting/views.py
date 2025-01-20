from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Question, Voting
from .serializers import QuestionSerializer, VotingSerializer

# Create your views here.

class QuestionListCreateView(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all().order_by('-vote_count')

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        phone_number = request.data.get('phone_number')
        question_text = request.data.get('question_text')
        vote_count = 0
        # Check if user already has a question with the same phone number
        existing_question = Question.objects.filter(
            phone_number=phone_number
        ).first()
        
        if existing_question:
            return Response(
                {"error": "You have already submitted a question with this phone number"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        question = Question.objects.create(name=name, phone_number=phone_number, question_text=question_text, vote_count=vote_count)
        question.save()
        # Serialize the created question
        serializer = self.get_serializer(question)
        return Response(
            serializer.data,  # Return the serialized question data
            status=status.HTTP_201_CREATED
        )

       

class VotingCreateView(generics.CreateAPIView):
    serializer_class = VotingSerializer
    
    def create(self, request, *args, **kwargs):
        question_id = kwargs.get('question_id')  # Get question_id from URL
        name = request.data.get('name')
        phone_number = request.data.get('phone_number')
        
        # Check if user has already voted for this question
        existing_vote = Voting.objects.filter(
            question_id=question_id,
            name=name,
            phone_number=phone_number
        ).first()
        
        if existing_vote:
            return Response(
                {"error": "You have already voted for this question"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if the voter is the creator of the question
        question = Question.objects.filter(id=question_id).first()
        if question and question.phone_number == phone_number:
            return Response(
                {"error": "You cannot vote for your own question"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Add question_id to the request data
        data = request.data.copy()
        data['question'] = question_id
        
        # Create the vote and increment question vote count
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            try:
                question.vote_count += 1
                question.save()
                
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Question.DoesNotExist:
                return Response(
                    {"error": "Question not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
