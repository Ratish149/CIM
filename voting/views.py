from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Question, Voting, Session, RunningSession
from .serializers import QuestionSerializer, VotingSerializer, SessionSerializer, RunningSessionSerializer

# Create your views here.

class QuestionListCreateView(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all().order_by('-created_at')

    def create(self, request, *args, **kwargs):
        
        name = request.data.get('name')
        phone_number = request.data.get('phone_number')
        question_text = request.data.get('question_text')
        vote_count = 0

        # Check if the current running session is accepting questions
        running_session = RunningSession.objects.first()  # Assuming you want to check the first running session
        if running_session and not running_session.session.is_acepting_questions:
            return Response(
                {"error": "Cannot add question, session is not accepting questions"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the question and associate it with the current running session
        question = Question.objects.create(
            name=name,
            phone_number=phone_number,
            question_text=question_text,
            vote_count=vote_count
        )
        running_session.session.questions.add(question)  # Associate the question with the running session
        
        # Serialize the created question
        serializer = self.get_serializer(question)
        return Response(
            serializer.data,  # Return the serialized question data
            status=status.HTTP_201_CREATED
        )

class TopQuestionView(generics.ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        running_session = RunningSession.objects.first()  # Get the first running session
        if running_session:
            return Question.objects.filter(session=running_session.session).order_by('-vote_count')
        return Question.objects.none()  # Return an empty queryset if no running session exists

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

class QuestionsByRunningSessionView(generics.ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        running_session=RunningSession.objects.first()
        return Question.objects.filter(session__runningsession__id=running_session.id).order_by('-created_at')

class SessionListCreateView(generics.ListCreateAPIView):
    serializer_class = SessionSerializer
    queryset = Session.objects.all().order_by('-id')

class RunningSessionListCreateView(generics.ListCreateAPIView):
    serializer_class = RunningSessionSerializer
    queryset = RunningSession.objects.all().order_by('-id')

class RunningSessionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RunningSessionSerializer
    queryset = RunningSession.objects.all()
