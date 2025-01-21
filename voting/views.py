from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Question, Voting, Session, RunningSession
from .serializers import QuestionSerializer, VotingSerializer, SessionSerializer, RunningSessionSerializer, SessionOnlySerializer

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
        if not running_session:
            return Response(
                {"error": "No running session available"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not running_session.session.is_acepting_questions:
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
        if not running_session:
            return Response(
                {"error": "No running session available"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Question.objects.filter(session=running_session.session).order_by('-vote_count')

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
                # Check if there is a running session
        running_session = RunningSession.objects.first()
        if not running_session:
            return Response(
                {"error": "No running session available"},
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
        running_session = RunningSession.objects.first()
        if not running_session:
            return Question.objects.none()  # Return an empty queryset if no running session exists
        return Question.objects.filter(session__runningsession__id=running_session.id).order_by('-created_at')

class SessionListCreateView(generics.ListCreateAPIView):
    serializer_class = SessionSerializer
    queryset = Session.objects.all().order_by('-id')

    def get_serializer_class(self):
        return SessionOnlySerializer  # Use SessionOnlySerializer for GET requests

class RunningSessionListCreateView(generics.ListCreateAPIView):
    serializer_class = RunningSessionSerializer
    queryset = RunningSession.objects.all().order_by('-id')

class RunningSessionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RunningSessionSerializer
    queryset = RunningSession.objects.all()

    def update(self, request, *args, **kwargs):
        # Get the new session ID from the URL
        new_session_id = kwargs.get('session_id')
        
        if new_session_id:
            # Check if there is already a running session
            current_running_session = RunningSession.objects.first()
            if current_running_session:
                # Check if the new session is the same as the current running session
                if current_running_session.session.id == new_session_id:
                    return Response({"error": "This session is already running."}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    # Optionally, delete the current running session if you want to replace it
                    current_running_session.delete()

            # Create a new session instance
            new_session = Session.objects.filter(id=new_session_id).first()
            if new_session:
                # Create a new running session with the new session
                new_running_session = RunningSession.objects.create(session=new_session)
                return Response(
                    RunningSessionSerializer(new_running_session).data,
                    status=status.HTTP_201_CREATED
                )
            return Response({"error": "New session not found"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"error": "New session ID is required"}, status=status.HTTP_400_BAD_REQUEST)

class UpdateSessionAcceptingQuestionsView(generics.UpdateAPIView):
    serializer_class = SessionSerializer  # Assuming you want to use the same serializer
    queryset = RunningSession.objects.all()

    def update(self, request, *args, **kwargs):
        # Get the current running session
        running_session = RunningSession.objects.first()  # Assuming you want to check the first running session
        if running_session:
            # Toggle the is_accepting_questions value
            running_session.session.is_acepting_questions = not running_session.session.is_acepting_questions
            running_session.session.save()  # Save the updated session
            
            # Serialize the updated session
            serializer = self.get_serializer(running_session.session)
            return Response(
                {"message": "Session updated successfully", "session": serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(
            {"error": "No running session available"},
            status=status.HTTP_404_NOT_FOUND
        )
