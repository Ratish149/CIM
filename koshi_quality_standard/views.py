from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from django.db import models
import csv

from rest_framework.response import Response as DRFResponse
from .models import Question, Requirement, Response
from .serializers import RequirementSerializer, RequirementAnswerSerializer, FileUploadSerializer
from rest_framework import filters

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
                name=name,  # Use the extracted name
                email=email,  # Use the extracted email
                phone=phone,  # Use the extracted phone
                response_data=serializer.validated_data,  # Store the validated data
                earned_points=earned_points
            )
            response_instance.save()  # Save the instance to the database

            return DRFResponse(
                {
                    "total_points": total_points,
                    "earned_points": earned_points,
                },
                status=status.HTTP_200_OK,
            )
        return DRFResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

