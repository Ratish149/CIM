from django.conf import settings  # Import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Newsletter
from .serializers import ContactSerializer, NewsletterSerializer

# Create your views here.


class ContactView(APIView):
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            contact = serializer.save()

            # Send email to admin with contact details
            email_subject = "New Contact Received"
            context = {"contact": contact}
            html_message = render_to_string(
                "email_templates/contact_notification.html", context
            )
            plain_message = strip_tags(html_message)

            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [settings.ADMIN_EMAIL]

            # Create and send the email
            msg = EmailMultiAlternatives(
                subject=email_subject,
                body=plain_message,
                from_email=from_email,
                to=to_email,
            )
            msg.attach_alternative(html_message, "text/html")
            msg.send(fail_silently=False)

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
            return Response(
                {"message": "Successfully unsubscribed."}, status=status.HTTP_200_OK
            )
        except Newsletter.DoesNotExist:
            return Response(
                {"error": "Email not found."}, status=status.HTTP_404_NOT_FOUND
            )
