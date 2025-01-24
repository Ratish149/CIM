from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from .models import Contact, Newsletter
from .serializers import ContactSerializer, NewsletterSerializer
from django.conf import settings  # Import settings
from rest_framework import serializers

# Create your views here.

class ContactView(APIView):

    class ContactSerializer(serializers.ModelSerializer):  # Nested serializer class
        class Meta:
            model = Contact
            fields = ['name', 'email', 'phone_number', 'message','created_at']  # Specify the fields to be serialized

    def post(self, request):
        serializer = self.ContactSerializer(data=request.data)  # Use the nested ContactSerializer
        if serializer.is_valid():
            contact = serializer.save()
            # Send email to admin with contact details
            email_subject = 'New Contact Received'
            email_body = (
                f'Dear Admin,\n\n'
                f'A new contact submission has been received:\n\n'
                f'Name: {contact.name}\n'
                f'Email: {contact.email}\n'
                f'Phone Number: {contact.phone_number}\n'
                f'Message: {contact.message}\n'
                f'Created At: {contact.created_at}\n\n'
                'Please review the details and follow up with the contact as necessary.\n\n'
   
            )
            send_mail(
                email_subject,
                email_body,
                settings.DEFAULT_FROM_EMAIL,  # Use the default sender email from settings
                [settings.EMAIL_HOST_USER],  # Replace with the admin's email address
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
