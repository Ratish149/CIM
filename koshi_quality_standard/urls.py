from django.urls import path
from .views import QuestionListCreateView, AnswerListCreateView 

urlpatterns = [
    path('questions/', QuestionListCreateView.as_view(), name='question-list-create'),
    path('answers/', AnswerListCreateView.as_view(), name='answer-list-create'),
]