from django.urls import path
from .views import ContactView, NewsletterView,UnsubscribeAPIView

urlpatterns = [
    path('contact/', ContactView.as_view(), name='contact'),
    path('newsletter/', NewsletterView.as_view(), name='newsletter'),
    path('unsubscribe/<str:email>/', UnsubscribeAPIView.as_view(), name='unsubscribe'),

]
