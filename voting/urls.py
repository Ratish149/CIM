from django.urls import path
from .views import QuestionListCreateView, VotingCreateView, TopQuestionView

urlpatterns = [
    path('questions/', QuestionListCreateView.as_view(), name='question-list-create'),
    path('questions/<int:question_id>/vote/', VotingCreateView.as_view(), name='vote-create'),
    path('top-questions/', TopQuestionView.as_view(), name='top-questions'),
]
