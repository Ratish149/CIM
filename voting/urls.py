from django.urls import path
from .views import QuestionListCreateView, VotingCreateView, TopQuestionView, QuestionsByRunningSessionView, SessionListCreateView, RunningSessionListCreateView, RunningSessionRetrieveUpdateDestroyView

urlpatterns = [
    path('questions/', QuestionListCreateView.as_view(), name='question-list-create'),
    path('questions/<int:question_id>/vote/', VotingCreateView.as_view(), name='vote-create'),
    path('top-questions/', TopQuestionView.as_view(), name='top-questions'),
    path('running-session/questions/', QuestionsByRunningSessionView.as_view(), name='questions_by_running_session'),
    path('sessions/', SessionListCreateView.as_view(), name='session_list_create'),
    path('running-sessions/', RunningSessionListCreateView.as_view(), name='running-session-list-create'),
    path('running-sessions/<int:pk>/', RunningSessionRetrieveUpdateDestroyView.as_view(), name='running-session-retrieve-update-destroy'),
]
