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

# Create your views here.

class RequirementListView(generics.ListAPIView):
    queryset = Requirement.objects.all().order_by('id')
    serializer_class = RequirementSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class CalculatePointsView(APIView):
    def post(self, request, *args, **kwargs):
        # Extract additional fields from the request
        name = request.data.get('name', '')
        email = request.data.get('email', '')
        phone = request.data.get('phone', '')
        requirements_data = request.data.get('requirements', [])

        # Validate the requirements data
        serializer = RequirementAnswerSerializer(data=requirements_data, many=True)
        if serializer.is_valid():
            total_points = Question.objects.aggregate(total=models.Sum('points'))['total'] or 0
            earned_points = 0

            for requirement_data in serializer.validated_data:
                requirement_id = requirement_data['requirement_id']
                is_relevant = requirement_data['is_relevant']

                if not is_relevant:
                    # Deduct points for all questions in the skipped requirement
                    skipped_points = Question.objects.filter(requirement_id=requirement_id).aggregate(
                        total=models.Sum('points')
                    )['total'] or 0
                    total_points -= skipped_points
                else:
                    # Process answers if the requirement is relevant
                    answers = requirement_data.get('answers', [])
                    for answer in answers:
                        question_id = answer['question_id']  # No need for .get() as it's validated
                        question_answer = answer['answer']

                        try:
                            question = Question.objects.get(id=question_id)

                            if question_answer is True:
                                earned_points += question.points
                            # No need for an else clause since False adds 0
                        except Question.DoesNotExist:
                            return DRFResponse(
                                {"error": f"Question with ID {question_id} does not exist."},
                                status=status.HTTP_404_NOT_FOUND,
                            )

            # Save the response data to the database using the custom Response model
            response_instance = Response(
                name=name,
                email=email,
                phone=phone,
                response_data=serializer.validated_data,
                earned_points=earned_points
            )
            response_instance.save()

            # Generate PDF
            pdf_content = self.generate_pdf(name, email, phone, serializer.validated_data, total_points, earned_points)

            # Send email with the PDF
            self.send_email_with_pdf(name, email, pdf_content, total_points, earned_points)

            return DRFResponse(
                {
                    "total_points": total_points,
                    "earned_points": earned_points,
                },
                status=status.HTTP_200_OK,
            )
        return DRFResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def generate_pdf(self, name, email, phone, requirements_data, total_points, earned_points):
        enriched_data = []
        for req in requirements_data:
            requirement_id = req['requirement_id']
            requirement_name = Requirement.objects.get(id=requirement_id).name  # Fetch requirement name
            is_relevant = req['is_relevant']  # Get the relevance status
            answers = []
            
            for ans in req.get('answers', []):  # Use .get() to handle cases with no answers
                question_id = ans['question_id']
                question = Question.objects.get(id=question_id)
                answers.append({
                    'question_id': question_id,
                    'question_name': question.text,  # Fetch question name
                    'answer': "Yes" if ans['answer'] else "No",  # Convert boolean to Yes/No
                })
            
            # Calculate rowspan
            rowspan = len(answers) if answers else 1
            enriched_data.append({
                'requirement_id': requirement_id,
                'requirement_name': requirement_name,
                'is_relevant': is_relevant,
                'answers': answers,
                'rowspan': rowspan,
            })

        html_template = 'pdf/pdf_template.html'
        context = {
            'name': name,
            'email': email,
            'phone': phone,
            'requirements_data': enriched_data,
            'total_points': total_points,
            'earned_points': earned_points,
        }

        # Render the HTML template with context
        html_content = render_to_string(html_template, context)
        pdf_buffer = BytesIO()

        # Create PDF
        pisa_status = pisa.CreatePDF(html_content, dest=pdf_buffer)
        if pisa_status.err:
            raise Exception("PDF generation failed")

        pdf_buffer.seek(0)
        return pdf_buffer.getvalue()

    def send_email_with_pdf(self, name, email, pdf_content, total_points, earned_points):
        from django.conf import settings  # Import settings

        email_subject = "Your Response Summary"
        email_body = render_to_string('mail/email_template.html', {
            'name': name,
            'total_points': total_points,
            'earned_points': earned_points,
        })
        email_message = EmailMessage(
            subject=email_subject,
            body=email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,  # Use default email from settings
            to=[email],
        )
        email_message.attach(f'{name}_summary.pdf', pdf_content, 'application/pdf')
        email_message.content_subtype = 'html'  # Set email body content as HTML
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

