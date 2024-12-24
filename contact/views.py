from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from .models import Contact, Newsletter
from .serializers import ContactSerializer, NewsletterSerializer
from django.conf import settings  # Import settings

# Create your views here.

class ContactView(APIView):
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            contact = serializer.save()
            # Send email
            send_mail(
                'Thank you for contacting us!',
                f'Hello {contact.name},\n\nThank you for reaching out! We have received your message:\n\n"{contact.message}"\n\nWe will get back to you shortly.\n\nBest regards,\nYour Company',
                settings.DEFAULT_FROM_EMAIL,  # Use the default sender email from settings
                [contact.email],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewsletterView(APIView):
    def post(self, request):
        serializer = NewsletterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UnsubscribeAPIView(APIView):
    def post(self, request, email):
        try:
            newsletter = Newsletter.objects.get(email=email)
            newsletter.subscribed = False
            newsletter.save()
            return Response({"message": "Successfully unsubscribed."}, status=status.HTTP_200_OK)
        except Newsletter.DoesNotExist:
            return Response({"error": "Email not found."}, status=status.HTTP_404_NOT_FOUND)
