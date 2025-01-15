from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from django.db import models
import csv

from rest_framework.response import Response as DRFResponse
from .models import Question, Requirement, Response
from .serializers import RequirementSerializer, RequirementAnswerSerializer, FileUploadSerializer
from rest_framework import filters
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO
from datetime import datetime
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

        serializer = RequirementAnswerSerializer(data=requirements_data, many=True)
        if serializer.is_valid():
            total_points = 417
            earned_points = 0

            for requirement_data in serializer.validated_data:
                requirement_id = requirement_data["requirement_id"]
                is_relevant = requirement_data["is_relevant"]

                if not is_relevant:
                    skipped_points = Question.objects.filter(requirement_id=requirement_id).aggregate(
                        total=models.Sum("points")
                    )["total"] or 0
                    total_points -= skipped_points
                else:
                    answers = requirement_data.get("answers", [])
                    for answer in answers:
                        question_id = answer["question_id"]
                        question_answer = answer["answer"]

                        try:
                            question = Question.objects.get(id=question_id)
                            if question_answer is True and question.points is not None:
                                earned_points += question.points
                        except Question.DoesNotExist:
                            return DRFResponse(
                                {"error": f"Question with ID {question_id} does not exist."},
                                status=status.HTTP_404_NOT_FOUND,
                            )

            response_instance = Response(
                name=name,
                email=email,
                phone=phone,
                response_data=serializer.validated_data,
                earned_points=earned_points,
            )
            response_instance.save()

            # Generate the paginated PDF
            pdf_content = self.generate_pdf(name, email, phone, serializer.validated_data, total_points, earned_points)
            
            # Add this new line to send email
            self.send_email_with_pdf(name, email, pdf_content, total_points, earned_points)

            return DRFResponse(
                {
                    "total_points": total_points,
                    "earned_points": earned_points,
                },
                status=status.HTTP_200_OK,
            )
        return DRFResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def paginate_data(self, data, items_per_page=10):
        """Split data into smaller chunks for pagination."""
        for i in range(0, len(data), items_per_page):
            yield data[i:i + items_per_page]

    def generate_pdf(self, name, email, phone, requirements_data, total_points, earned_points):
        """Generate paginated PDFs to handle large data."""
        current_year = datetime.now().year
        paginated_data = list(self.paginate_data(requirements_data, items_per_page=10))  # 10 items per page
        pdf_buffer = BytesIO()

        for page_index, page_data in enumerate(paginated_data, start=1):
            context = {
                "name": name,
                "email": email,
                "phone": phone,
                "requirements_data": page_data,
                "total_points": total_points,
                "earned_points": earned_points,
                "current_year": current_year,
                "page_number": page_index,
                "total_pages": len(paginated_data),
            }

            html_content = render_to_string("pdf/pdf_template.html", context)
            pisa.CreatePDF(html_content, dest=pdf_buffer, encoding="UTF-8")

        if pdf_buffer.getvalue():
            pdf_buffer.seek(0)
            return pdf_buffer.getvalue()
        raise Exception("PDF generation failed")

    def send_email_with_pdf(self, name, email, pdf_content, total_points, earned_points):
        """Send an email with the generated PDF attached."""
        email_subject = "Your Response Summary"
        email_body = render_to_string('mail/email_template.html', {
            'name': name,
            'total_points': total_points,
            'earned_points': earned_points,
        })

        email_message = EmailMessage(
            subject=email_subject,
            body=email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )
        email_message.attach(f"{name}_response_summary.pdf", pdf_content, "application/pdf")
        email_message.content_subtype = "html"  # Set email body content as HTML

        try:
            email_message.send()
        except Exception as e:
            raise Exception(f"Failed to send email: {str(e)}")


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

