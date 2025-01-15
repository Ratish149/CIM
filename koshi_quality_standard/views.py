from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from django.db import models
import csv

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

        total_points = 417
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
                        earned_points += question.points or 0
                        answers.append({
                            "question_name": question.text,
                            "answer": "Yes" if answer_data.get("answer") else "No"
                        })
                enriched_data.append({
                    "requirement_name": requirement_name,
                    "answers": answers
                })

        # Save the response data
        Response.objects.create(
            name=name,
            email=email,
            phone=phone,
            response_data=requirements_data,  # Save the original requirements data
            earned_points=earned_points
        )

        self.send_email_with_summary(name, email, enriched_data, total_points, earned_points)

        return DRFResponse({
            "total_points": total_points,
            "earned_points": earned_points,
            "message": "Summary sent successfully!"
        }, status=status.HTTP_200_OK)

    def send_email_with_summary(self, name, email, enriched_data, total_points, earned_points):
        subject = "Response Summary"
        body = render_to_string("mail/email_template.html", {
            "name": name,
            "enriched_data": enriched_data,
            "total_points": total_points,
            "earned_points": earned_points
        })
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [email]

        email_message = EmailMessage(
            subject=subject,
            body=body,
            from_email=from_email,
            to=to_email,
        )
        email_message.content_subtype = "html"
        email_message.send()

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

