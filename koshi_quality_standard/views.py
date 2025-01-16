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
from .models import Question, Requirement, Response
from .serializers import RequirementSerializer, FileUploadSerializer
from rest_framework import filters
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

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
        points_ratio = earned_points / 100
        category = ''
        percentage = 0

        if 0 <= points_ratio <= 1:
            category = 'a'
            percentage = 20
        elif 1 < points_ratio <= 2:
            category = 'b'
            percentage = 40
        elif 2 < points_ratio <= 3:
            category = 'c'
            percentage = 60
        elif 3 < points_ratio <= 4:
            category = 'd'
            percentage = 80
        else:  # points_ratio > 4
            category = 'e'
            percentage = 100

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
        if percentage >= 20 and category != 'a':
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
                "percentage": percentage
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
                "percentage": percentage
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

