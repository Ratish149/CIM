from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from django.db import models
import csv
import os
import fitz
from datetime import datetime
from nepali_datetime import date as nepali_datetime

from rest_framework.response import Response as DRFResponse
from .models import Question, Requirement, Response,ContactForm
from .serializers import RequirementSerializer, FileUploadSerializer,ContactFormSerializer
from rest_framework import filters
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import strip_tags
from rest_framework.permissions import AllowAny

# Create your views here.

class RequirementListView(generics.ListAPIView):
    queryset = Requirement.objects.all().order_by('id')
    serializer_class = RequirementSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']



class CalculatePointsView(APIView):
    def post(self, request, *args, **kwargs):
        name = request.data.get("name", "")
        email = request.data.get("email", "")
        phone = request.data.get("phone", "")
        requirements_data = request.data.get("requirements", [])

        total_points = 412
        earned_points = 0
        enriched_data = []

        for requirement_data in requirements_data:
            requirement_id = requirement_data.get("requirement_id")
            is_relevant = requirement_data.get("is_relevant", False)
            requirement_name = Requirement.objects.filter(id=requirement_id).first().name if requirement_id else "Unknown"

            if not is_relevant:
                skipped_points = Question.objects.filter(requirement_id=requirement_id).aggregate(
                    total=models.Sum("points")
                )["total"] or 0
                total_points -= skipped_points
            else:
                answers = []
                for answer_data in requirement_data.get("answers", []):
                    question_id = answer_data.get("question_id")
                    question = Question.objects.filter(id=question_id).first()
                    if question:
                        # Only add points if answer is True
                        if answer_data.get("answer"):
                            earned_points += question.points or 0
                        answers.append({    
                            "question_name": question.text,
                            "answer": "Yes" if answer_data.get("answer") else "No"
                        })
                enriched_data.append({
                    "requirement_name": requirement_name,
                    "answers": answers
                })

        # Calculate category based on earned_points/100
        points_ratio = round((earned_points / total_points) * 100, 2)  # Round to 2 decimal places
        category = ''
        percentage = 0

        if 0 <= points_ratio <= 20:
            category = 'e'
            percentage = points_ratio
        elif 20 < points_ratio <= 40:
            category = 'd'
            percentage = points_ratio
        elif 40 < points_ratio <= 60:
            category = 'c'
            percentage = points_ratio
        elif 60 < points_ratio <= 80:
            category = 'b'
            percentage = points_ratio
        else:  # points_ratio > 80
            category = 'a'
            percentage = points_ratio

        # Create Response instance
        response_instance = Response.objects.create(
            name=name,
            email=email,
            phone=phone,
            response_data=requirements_data,
            earned_points=earned_points,
            category=category,
            percentage=percentage
        )

        file_url = None
        # Only create PDF if percentage >= 20 and category is not 'a'
        if percentage >= 20 and category != 'e':
            # Create pdf directory if it doesn't exist
            output_dir = "media/pdf/QHSEF/"
            os.makedirs(output_dir, exist_ok=True)
            output_pdf = f"{output_dir}QHSEF_{response_instance.id}.pdf"

            # Define the path to the input PDF template
            input_pdf = "media/QHSEF_edit.pdf"  # Make sure this template exists

            # Convert date to Nepali
            english_date = response_instance.created_at
            nepali_date_str = nepali_datetime.from_datetime_date(english_date.date()).strftime('%B %d, %Y')

            # Data to populate the form fields
            field_data = {
                'ChalanNo': f"2081/82 - {response_instance.id}",
                'Name': response_instance.name,
                'Email': response_instance.email,
                'Phone': response_instance.phone,
                'Category': f"Category {category.upper()}",
                'Percentage': f"{percentage}%",
                'EarnedPoints': str(earned_points),
                'TotalPoints': str(total_points),
                'CreatedAt': nepali_date_str
            }

            # Fill the PDF
            pdf = fitz.open(input_pdf)
            for page_num in range(len(pdf)):
                page = pdf[page_num]
                widgets = page.widgets()
                if widgets:
                    for widget in widgets:
                        if widget.field_name in field_data:
                            widget.field_value = field_data[widget.field_name]
                            widget.update()

            # Save the updated PDF
            pdf.save(output_pdf)
            pdf.close()

            # Build the file URL
            file_url = request.build_absolute_uri(f"/media/pdf/QHSEF/QHSEF_{response_instance.id}.pdf")

            # Save the file URL
            response_instance.file_url = file_url
            response_instance.save()

            # Send email with PDF attachment
            subject = "Response Summary"
            body = render_to_string("mail/email_template.html", {
                "name": name,
                "enriched_data": enriched_data,
                "total_points": total_points,
                "earned_points": earned_points,
                "category": category,
                "percentage": percentage,
                "response_id": response_instance.id
            })

            email_message = EmailMessage(
                subject=subject,
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email],
            )

            # Attach the generated PDF
            with open(output_pdf, 'rb') as pdf_file:
                email_message.attach(f'QHSEF_{response_instance.id}.pdf', 
                                   pdf_file.read(), 
                                   'application/pdf')

            email_message.content_subtype = "html"
            email_message.send()

        else:
            # Send email without PDF attachment
            subject = "Response Summary"
            body = render_to_string("mail/email_template.html", {
                "name": name,
                "enriched_data": enriched_data,
                "total_points": total_points,
                "earned_points": earned_points,
                "category": category,
                "percentage": percentage,
                "response_id": response_instance.id
            })

            email_message = EmailMessage(
                subject=subject,
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email],
            )
            email_message.content_subtype = "html"
            email_message.send()

        return DRFResponse({
            "total_points": total_points,
            "earned_points": earned_points,
            "category": category,
            "percentage": percentage,
            "file_url": file_url,
            "message": "Summary sent successfully!"
        }, status=status.HTTP_200_OK)

class RequirementQuestionBulkUploadView(APIView):
    serializer_class = FileUploadSerializer
    def post(self, request, *args, **kwargs):
        csv_file = request.FILES.get('file')
        if not csv_file:
            return DRFResponse({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Decode the file to a text stream and parse it
            file_data = csv_file.read().decode('utf-8-sig').splitlines()  # Handle BOM if present
            reader = csv.DictReader(file_data)

            success_count = 0
            skip_count = 0

            for row in reader:
                requirement_name = row.get('requirement')
                question_text = row.get('question')
                points = row.get('points')

                if not requirement_name or not question_text or not points:
                    skip_count += 1
                    continue

                try:
                    # Ensure points is a float
                    points = float(points)

                    # Create or get the requirement
                    requirement, _ = Requirement.objects.get_or_create(name=requirement_name)

                    # Check for duplicate questions under the same requirement
                    if Question.objects.filter(requirement=requirement, text=question_text).exists():
                        skip_count += 1
                        continue

                    # Create the question
                    Question.objects.create(
                        requirement=requirement,
                        text=question_text,
                        points=points
                    )
                    success_count += 1

                except Exception as e:
                    skip_count += 1
                    print(f"Failed to insert row: {row}. Error: {e}")  # Debugging

            return DRFResponse({
                "message": "CSV file data uploaded successfully!",
                "records_created": success_count,
                "records_skipped": skip_count
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return DRFResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ResponseDetailView(generics.RetrieveAPIView):
    queryset = Response.objects.all()
    permission_classes = [AllowAny]  # You might want to add authentication later
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Parse the stored response_data to get requirement details
        enriched_data = []
        for requirement_data in instance.response_data:
            if requirement_data.get("is_relevant", False):
                requirement_id = requirement_data.get("requirement_id")
                requirement_name = Requirement.objects.filter(id=requirement_id).first().name if requirement_id else "Unknown"
                
                answers = []
                for answer_data in requirement_data.get("answers", []):
                    question_id = answer_data.get("question_id")
                    question = Question.objects.filter(id=question_id).first()
                    if question:
                        answers.append({
                            "question": question.text,
                            "answer": "Yes" if answer_data.get("answer") else "No",
                            "points": question.points if answer_data.get("answer") else 0
                        })
                
                enriched_data.append({
                    "requirement_name": requirement_name,
                    "answers": answers
                })

        return DRFResponse({
            "id": instance.id,
            "name": instance.name,
            "email": instance.email,
            "phone": instance.phone,
            "earned_points": instance.earned_points,
            "category": instance.category,
            "percentage": instance.percentage,
            "file_url": instance.file_url,
            "created_at": instance.created_at,
            "requirements": enriched_data
        }, status=status.HTTP_200_OK)


class ContactFormListCreateView(generics.ListCreateAPIView):
    queryset = ContactForm.objects.all()
    serializer_class = ContactFormSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Prepare context for email template
        context = {
            'name': serializer.validated_data['name'],
            'email': serializer.validated_data['email'],
            'phone_number': serializer.validated_data['phone_number'],
            'subject': serializer.validated_data['subject'],
            'message': serializer.validated_data['message']
        }

        # Render the HTML template
        html_message = render_to_string(
            'mail/qhsef_contact.html',
            context
        )

        # Send email to admin
        subject = f"New Contact Form Submission: {serializer.validated_data['subject']}"
        from_email = settings.DEFAULT_FROM_EMAIL
        
        # Update recipient_list to include the specified email
        recipient_list = ['biratexpo2025@gmail.com']  # Updated recipient list
        
        # Send both HTML and plain text versions
        send_mail(
            subject=subject,
            message=strip_tags(html_message),  # Plain text version
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message  # HTML version
        )

        return DRFResponse({"message": "Contact form submitted successfully."})