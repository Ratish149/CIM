import csv
from io import TextIOWrapper

from django.db import models
from django.db.models import F, Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters import rest_framework as django_filters
from rest_framework import filters, generics, parsers, permissions, status, views
from rest_framework.exceptions import APIException, NotFound, ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from jobbriz.serializers import WorkInterestListSerializer

from .models import (
    ApprenticeshipApplication,
    CareerHistory,
    Certification,
    Education,
    HireRequest,
    InternshipIndustry,
    JobApplication,
    JobPost,
    JobSeeker,
    Language,
    Location,
    MajorGroup,
    MinorGroup,
    SavedJob,
    Skill,
    SubMajorGroup,
    UnitGroup,
    WorkInterest,
    WorkInterestHire,
)
from .serializers import (
    ApprenticeshipApplicationSerializer,
    CareerHistorySerializer,
    CertificationSerializer,
    EducationSerializer,
    HireRequestSerializer,
    HireRequestStatusUpdateSerializer,
    ImportGroupsSerializer,
    InternshipIndustrySerializer,
    InternshipRegistrationSerializer,
    JobApplicationSerializer,
    JobApplicationStatusUpdateSerializer,
    JobListAllSerializer,
    JobPostDetailSerializer,
    JobPostListSerializer,
    JobSeekerSerializer,
    JobSeekerSerializer2,
    LanguageSerializer,
    LocationSerializer,
    MajorGroupSerializer,
    MinorGroupSerializer,
    SavedJobSerializer,
    SkillSerializer,
    SubMajorGroupSerializer,
    UnitGroupSerializer,
    UserSerializer,
    WorkInterestHireSerializer,
    WorkInterestSerializer,
)
from .utils import (
    send_apprenticeship_application_emails,
    send_internship_registration_emails,
    send_job_application_emails,
    send_work_interest_hire_emails,
)


class HasJobseekerProfileView(APIView):
    def get(self, request):
        return Response(JobSeeker.objects.filter(user=request.user).exists())


class JobSeekerListCreateView(generics.ListCreateAPIView):
    queryset = JobSeeker.objects.all()
    serializer_class = JobSeekerSerializer2
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class JobSeekerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobSeeker.objects.all()
    serializer_class = JobSeekerSerializer2
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        try:
            return JobSeeker.objects.get(user=self.request.user)
        except JobSeeker.DoesNotExist:
            raise NotFound(
                {"code": "profile_not_found", "message": "JobSeeker profile not found."}
            )

    def get_serializer_class(self):
        if (
            self.request.method == "PATCH"
            or self.request.method == "PUT"
            or self.request.method == "POST"
        ):
            return JobSeekerSerializer
        return JobSeekerSerializer2


class LocationListCreateView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class IndustryListCreateView(generics.ListCreateAPIView):
    queryset = InternshipIndustry.objects.all()
    serializer_class = InternshipIndustrySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class LanguageListCreateView(generics.ListCreateAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class InternshipRegistrationView(generics.ListCreateAPIView):
    """
    API view to register a new user and create an internship profile in one call.
    """

    queryset = JobSeeker.objects.all()
    serializer_class = InternshipRegistrationSerializer
    permission_classes = (permissions.AllowAny,)
    parser_classes = (parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser)

    def perform_create(self, serializer):
        # Save the job seeker profile
        job_seeker = serializer.save()

        # Send email notifications
        try:
            send_internship_registration_emails(job_seeker)
        except Exception as e:
            # Log error but don't fail the request
            print(f"Failed to send internship registration emails: {e}")


class CertificationListCreateView(generics.ListCreateAPIView):
    serializer_class = CertificationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # Get certification records associated with the user's JobSeeker profile
        return Certification.objects.filter(jobseeker__user=self.request.user)

    def perform_create(self, serializer):
        # Get the JobSeeker instance for the authenticated user
        try:
            job_seeker = JobSeeker.objects.get(user=self.request.user)
        except JobSeeker.DoesNotExist:
            raise ValidationError(
                "You must have a JobSeeker profile to add certification records."
            )

        # Create the certification record
        certification = serializer.save()
        # Add it to the JobSeeker's certifications
        job_seeker.certifications.add(certification)


class EducationListCreateView(generics.ListCreateAPIView):
    serializer_class = EducationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # Get education records associated with the user's JobSeeker profile
        return Education.objects.filter(jobseeker__user=self.request.user)

    def perform_create(self, serializer):
        # Get the JobSeeker instance for the authenticated user
        try:
            job_seeker = JobSeeker.objects.get(user=self.request.user)
        except JobSeeker.DoesNotExist:
            raise APIException(
                "You must have a JobSeeker profile to add education records."
            )

        # Check if the user already has this specific education record
        if job_seeker.education.filter(
            course_or_qualification=serializer.validated_data["course_or_qualification"]
        ).exists():
            raise APIException(
                "You have already added an education record for this course or qualification."
            )

        # Create the education record
        education = serializer.save()
        # Add it to the JobSeeker's education
        job_seeker.education.add(education)


class EducationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = (permissions.IsAuthenticated,)


class CareerHistoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CareerHistorySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # Get career history records associated with the user's JobSeeker profile
        return CareerHistory.objects.filter(job_seeker__user=self.request.user)

    def perform_create(self, serializer):
        # Get the JobSeeker instance for the authenticated user
        try:
            job_seeker = JobSeeker.objects.get(user=self.request.user)
        except JobSeeker.DoesNotExist:
            raise APIException(
                "You must have a JobSeeker profile to add career history records."
            )

        # Get the new career history data
        new_start_date = serializer.validated_data.get("start_date")
        new_end_date = serializer.validated_data.get("end_date")

        # Check if there is an ongoing career history record
        ongoing_records = job_seeker.career_history.filter(end_date__isnull=True)
        if ongoing_records.exists():
            raise APIException(
                "You must end your current career history before adding a new one."
            )

        # Check for overlapping career history records
        overlapping_records = job_seeker.career_history.filter(
            (Q(start_date__lte=new_end_date) & Q(end_date__gte=new_start_date))
            | (Q(start_date__gte=new_start_date) & Q(end_date__lte=new_end_date))
        )

        if overlapping_records.exists():
            raise APIException(
                "The new career history overlaps with existing records. Please adjust the dates."
            )

        # Create the career history record
        career_history = serializer.save()
        # Add it to the JobSeeker's career history
        job_seeker.career_history.add(career_history)


class SkillListCreateView(generics.ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

    def create(self, request, *args, **kwargs):
        data = request.data
        is_many = isinstance(data, list)

        if isinstance(data, str):
            # Handle single string input
            data = {"name": data}
            is_many = False
        elif is_many:
            # Handle list of strings input
            if data and isinstance(data[0], str):
                data = [{"name": item} for item in data]

        serializer = self.get_serializer(data=data, many=is_many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        # Save the skill first
        skill_or_skills = serializer.save()

        # Link to JobSeeker profile only if user is authenticated and has a profile
        if self.request.user.is_authenticated:
            try:
                job_seeker = JobSeeker.objects.get(user=self.request.user)
                if isinstance(skill_or_skills, list):
                    job_seeker.skills.add(*skill_or_skills)
                else:
                    job_seeker.skills.add(skill_or_skills)
            except JobSeeker.DoesNotExist:
                pass


class SkillDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = (permissions.IsAuthenticated,)


class CareerHistoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CareerHistory.objects.all()
    serializer_class = CareerHistorySerializer
    permission_classes = (permissions.IsAuthenticated,)


class CertificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
    permission_classes = (permissions.IsAuthenticated,)


class MajorGroupListCreateView(generics.ListCreateAPIView):
    queryset = MajorGroup.objects.all()
    serializer_class = MajorGroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "code"]


class MajorGroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MajorGroup.objects.all()
    serializer_class = MajorGroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "slug"


class SubMajorGroupListCreateView(generics.ListCreateAPIView):
    queryset = SubMajorGroup.objects.all()
    serializer_class = SubMajorGroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "code"]

    def get_queryset(self):
        major_groups = self.request.query_params.get("major_groups")
        if major_groups:
            major_group_list = major_groups.split(",")
            return SubMajorGroup.objects.filter(major_group__code__in=major_group_list)
        return SubMajorGroup.objects.all()


class SubMajorGroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubMajorGroup.objects.all()
    serializer_class = SubMajorGroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "slug"


class MinorGroupListCreateView(generics.ListCreateAPIView):
    queryset = MinorGroup.objects.all()
    serializer_class = MinorGroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "code"]

    def get_queryset(self):
        sub_major_groups = self.request.query_params.get("sub_major_groups")
        if sub_major_groups:
            sub_major_group_list = sub_major_groups.split(",")
            return MinorGroup.objects.filter(
                sub_major_group__code__in=sub_major_group_list
            )
        return MinorGroup.objects.all()


class MinorGroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MinorGroup.objects.all()
    serializer_class = MinorGroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "slug"


class UnitGroupListCreateView(generics.ListCreateAPIView):
    queryset = UnitGroup.objects.all()
    serializer_class = UnitGroupSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "code"]

    def get_queryset(self):
        minor_groups = self.request.query_params.get("minor_groups")
        if minor_groups:
            minor_group_list = minor_groups.split(",")
            return UnitGroup.objects.filter(minor_group__code__in=minor_group_list)
        return UnitGroup.objects.all()


class UnitGroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UnitGroup.objects.all()
    serializer_class = UnitGroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "slug"


class CustomPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = "page_size"
    max_page_size = 100


class JobPostListCreateView(generics.ListCreateAPIView):
    serializer_class = JobPostListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "description"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = JobListAllSerializer(
            result_page, many=True, context={"request": request}
        )
        return paginator.get_paginated_response(serializer.data)

    def get_queryset(self):
        queryset = JobPost.objects.filter(status="Published")

        # Keyword search
        keywords = self.request.query_params.get("keywords")
        if keywords:
            queryset = queryset.filter(
                models.Q(title__icontains=keywords)
                | models.Q(description__icontains=keywords)
                | models.Q(requirements__icontains=keywords)
            )

        # ISCO Classification filters
        major_groups = self.request.query_params.get("major_groups")
        sub_major_groups = self.request.query_params.get("sub_major_groups")
        minor_groups = self.request.query_params.get("minor_groups")
        unit_groups = self.request.query_params.get("unit_groups")

        classification_query = models.Q()

        if major_groups:
            major_group_list = major_groups.split(",")
            classification_query &= models.Q(
                unit_group__minor_group__sub_major_group__major_group__code__in=major_group_list
            )

        if sub_major_groups:
            sub_major_group_list = sub_major_groups.split(",")
            classification_query &= models.Q(
                unit_group__minor_group__sub_major_group__code__in=sub_major_group_list
            )

        if minor_groups:
            minor_group_list = minor_groups.split(",")
            classification_query &= models.Q(
                unit_group__minor_group__code__in=minor_group_list
            )

        if unit_groups:
            unit_group_list = unit_groups.split(",")
            classification_query &= models.Q(unit_group__code__in=unit_group_list)

        if classification_query:
            queryset = queryset.filter(classification_query)

        # Location filter
        location = self.request.query_params.get("location")
        if location:
            queryset = queryset.filter(location__icontains=location)

        # Employment type filter
        employment_type = self.request.query_params.get("employment_type")
        if employment_type and employment_type != "Any employment type":
            queryset = queryset.filter(employment_type=employment_type)

        # Salary range filter
        salary_min = self.request.query_params.get("salary_min")
        salary_max = self.request.query_params.get("salary_max")
        if salary_min:
            queryset = queryset.filter(salary_range_min__gte=salary_min)
        if salary_max:
            queryset = queryset.filter(salary_range_max__lte=salary_max)

        # Posted date filter
        listing_time = self.request.query_params.get("listing_time")
        if listing_time:
            if listing_time == "Last 24 hours":
                date_threshold = timezone.now() - timezone.timedelta(days=1)
            elif listing_time == "Last 3 days":
                date_threshold = timezone.now() - timezone.timedelta(days=3)
            elif listing_time == "Last 7 days":
                date_threshold = timezone.now() - timezone.timedelta(days=7)
            elif listing_time == "Last 14 days":
                date_threshold = timezone.now() - timezone.timedelta(days=14)
            elif listing_time == "Last 30 days":
                date_threshold = timezone.now() - timezone.timedelta(days=30)

            if date_threshold:
                queryset = queryset.filter(posted_date__gte=date_threshold)

        return queryset.order_by("-posted_date").distinct()

    def perform_create(self, serializer):
        unit_group = UnitGroup.objects.get(code=self.request.data.get("unit_group"))
        serializer.save(unit_group=unit_group, user=self.request.user)


class MyJobListView(generics.ListAPIView):
    serializer_class = JobListAllSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return JobPost.objects.filter(user=self.request.user)


class JobPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobPost.objects.all()
    serializer_class = JobPostDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "slug"


class JobPostViewCountView(views.APIView):
    def post(self, request, slug):
        job_post = get_object_or_404(JobPost, slug=slug)
        job_post.views_count = F("views_count") + 1
        job_post.save()
        return Response(status=status.HTTP_200_OK)


class JobApplicationCreateView(generics.CreateAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        print(self.request.data)
        print(self.request.user)
        job_slug = self.kwargs.get("job_slug")
        job = get_object_or_404(JobPost, slug=job_slug)

        # Check if user has already applied
        if JobApplication.objects.filter(job=job, applicant=self.request.user).exists():
            raise ValidationError("You have already applied for this job")

        # Create the application
        application = serializer.save(applicant=self.request.user, job=job)

        # Update the applications count atomically
        JobPost.objects.filter(pk=job.pk).update(
            applications_count=models.F("applications_count") + 1
        )

        # Send email notifications
        try:
            send_job_application_emails(application)
        except Exception as e:
            # Log error but don't fail the request
            print(f"Failed to send application emails: {e}")


class AppliedJobsView(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user:
            return JobApplication.objects.filter(applicant=user)
        return JobApplication.objects.none()


class JobApplicationListView(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user:
            return JobApplication.objects.filter(applicant=user)
        return JobApplication.objects.none()


class JobApplicationDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user:
            return JobApplication.objects.filter(applicant=user)
        return JobApplication.objects.none()


class UpdateApplicationStatusView(generics.UpdateAPIView):
    serializer_class = JobApplicationStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user:
            return JobApplication.objects.filter(applicant=user)
        return JobApplication.objects.none()


class SavedJobToggleView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, job_slug):
        if request.user.user_type != "Job Seeker":
            raise ValidationError("Only job seekers can save jobs")
        job = get_object_or_404(JobPost, slug=job_slug)
        saved_job, created = SavedJob.objects.get_or_create(
            job_seeker=request.user, job=job
        )

        if not created:
            saved_job.delete()
            return Response({"status": "removed"}, status=status.HTTP_200_OK)

        return Response({"status": "saved"}, status=status.HTTP_201_CREATED)


class SavedJobListView(generics.ListAPIView):
    serializer_class = SavedJobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, "jobseeker"):
            return SavedJob.objects.filter(job_seeker=self.request.user)
        return SavedJob.objects.none()


class HireRequestCreateView(generics.CreateAPIView):
    serializer_class = HireRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if user.user_type != "Employer":
            raise ValidationError("Only employers can create hire requests")

        job_slug = self.kwargs.get("job_slug")
        jobseeker_slug = self.kwargs.get("jobseeker_slug")

        job = get_object_or_404(JobPost, slug=job_slug)
        job_seeker = get_object_or_404(JobSeeker, slug=jobseeker_slug)

        if HireRequest.objects.filter(job=job, job_seeker=job_seeker.user).exists():
            raise ValidationError("A hire request already exists for this job seeker")

        serializer.save(job=job, job_seeker=job_seeker.user)


class HireRequestListView(generics.ListAPIView):
    serializer_class = HireRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user:
            return HireRequest.objects.filter(job_seeker=user)
        return HireRequest.objects.none()


class HireRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HireRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user:
            return HireRequest.objects.filter(job_seeker=user)
        return HireRequest.objects.none()


class HireRequestStatusUpdateView(generics.UpdateAPIView):
    serializer_class = HireRequestStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user:
            return HireRequest.objects.filter(job_seeker=user)
        return HireRequest.objects.none()


class UploadISCODataView(APIView):
    """
    API view to upload ISCO data from a CSV file.
    """

    serializer_class = ImportGroupsSerializer

    def post(self, request, *args, **kwargs):
        # Validate the incoming data using ImportGroupsSerializer
        serializer = ImportGroupsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Check if the file is provided
        csv_file = request.FILES.get("file")
        if not csv_file:
            return Response(
                {"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            csv_file_wrapper = TextIOWrapper(
                csv_file.file, encoding="utf-8-sig"
            )  # Handle BOM with utf-8-sig
            reader = csv.DictReader(csv_file_wrapper)

            # Normalize headers (strip spaces, remove BOM, etc.)
            reader.fieldnames = [
                field.strip().replace("\ufeff", "") for field in reader.fieldnames
            ]

            for row in reader:
                # Ensure required keys are present
                if (
                    "ISCO 08 Code" not in row
                    or "Title EN" not in row
                    or "Definition" not in row
                ):
                    return Response(
                        {"error": "Missing required fields in CSV row."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                code = row["ISCO 08 Code"].strip()
                title = row["Title EN"].strip()
                description = row["Definition"].strip()
                code_length = len(code)

                # Create or Get Major Group
                if code_length == 1:
                    major_group, _ = MajorGroup.objects.get_or_create(
                        code=code,
                        defaults={
                            "title": title,
                            "description": description,
                            "slug": f"major-{code}",
                        },
                    )

                # Create or Get Sub-Major Group
                elif code_length == 2:
                    major_group, _ = MajorGroup.objects.get_or_create(code=code[0])
                    sub_major_group, _ = SubMajorGroup.objects.get_or_create(
                        code=code,
                        major_group=major_group,
                        defaults={
                            "title": title,
                            "description": description,
                            "slug": f"sub-major-{code}",
                        },
                    )

                # Create or Get Minor Group
                elif code_length == 3:
                    sub_major_group, _ = SubMajorGroup.objects.get_or_create(
                        code=code[:2]
                    )
                    minor_group, _ = MinorGroup.objects.get_or_create(
                        code=code,
                        sub_major_group=sub_major_group,
                        defaults={
                            "title": title,
                            "description": description,
                            "slug": f"minor-{code}",
                        },
                    )

                # Create or Get Unit Group
                elif code_length == 4:
                    minor_group, _ = MinorGroup.objects.get_or_create(code=code[:3])
                    UnitGroup.objects.get_or_create(
                        code=code,
                        minor_group=minor_group,
                        defaults={
                            "title": title,
                            "description": description,
                            "slug": f"unit-{code}",
                        },
                    )

            return Response(
                {"message": "Data uploaded successfully."},
                status=status.HTTP_201_CREATED,
            )

        except MajorGroup.DoesNotExist:
            return Response(
                {"error": "MajorGroup matching query does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except SubMajorGroup.DoesNotExist:
            return Response(
                {"error": "SubMajorGroup matching query does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except MinorGroup.DoesNotExist:
            return Response(
                {"error": "MinorGroup matching query does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AllGroupsSearchView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        search_group = request.query_params.get("search_group", "").strip()

        if not search_group:
            return Response(
                {"error": "search_group parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Determine if search is by code (digits) or title (string)
        is_code_search = search_group.isdigit()

        if is_code_search:
            query = models.Q(code__startswith=search_group)
        else:
            query = models.Q(title__icontains=search_group)

        # Search in Major Groups (1-digit code)
        major_groups = MajorGroup.objects.filter(query).values("code", "title")

        # Search in Sub Major Groups (2-digit code)
        sub_major_groups = SubMajorGroup.objects.filter(query).values("code", "title")

        # Search in Minor Groups (3-digit code)
        minor_groups = MinorGroup.objects.filter(query).values("code", "title")

        # Search in Unit Groups (4-digit code)
        unit_groups = UnitGroup.objects.filter(query).values("code", "title")

        results = {
            "major_groups": [
                {"code": group["code"], "title": group["title"]}
                for group in major_groups
            ],
            "sub_major_groups": [
                {"code": group["code"], "title": group["title"]}
                for group in sub_major_groups
            ],
            "minor_groups": [
                {"code": group["code"], "title": group["title"]}
                for group in minor_groups
            ],
            "unit_groups": [
                {"code": group["code"], "title": group["title"]}
                for group in unit_groups
            ],
        }

        # Add count information
        counts = {
            "major_groups": len(results["major_groups"]),
            "sub_major_groups": len(results["sub_major_groups"]),
            "minor_groups": len(results["minor_groups"]),
            "unit_groups": len(results["unit_groups"]),
            "total": sum(len(groups) for groups in results.values()),
        }

        return Response({"counts": counts, "results": results})


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class ApprenticeshipApplicationCreateView(generics.CreateAPIView):
    """
    API view to create an apprenticeship application with multiple documents.
    """

    queryset = ApprenticeshipApplication.objects.all()
    serializer_class = ApprenticeshipApplicationSerializer
    permission_classes = (permissions.AllowAny,)
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)

    def perform_create(self, serializer):
        application = serializer.save()

        # Send email notifications
        try:
            send_apprenticeship_application_emails(application)
        except Exception as e:
            # Log error but don't fail the request
            print(f"Failed to send apprenticeship application emails: {e}")


class WorkInterestFilterSet(django_filters.FilterSet):
    unit_group = django_filters.NumberFilter(
        field_name="unit_group__id", lookup_expr="exact"
    )
    proficiency_level = django_filters.CharFilter(
        field_name="proficiency_level", lookup_expr="exact"
    )
    availability = django_filters.CharFilter(
        field_name="availability", lookup_expr="exact"
    )
    skills = django_filters.CharFilter(method="filter_skills")

    class Meta:
        model = WorkInterest
        fields = []

    def filter_skills(self, queryset, name, value):
        if not value:
            return queryset
        skill_names = [s.strip() for s in value.split(",") if s.strip()]
        if not skill_names:
            return queryset

        query = Q()
        for skill_name in skill_names:
            query |= Q(skills__name__icontains=skill_name)

        return queryset.filter(query).distinct()


class WorkInterestListCreateView(generics.ListCreateAPIView):
    queryset = WorkInterest.objects.all()
    serializer_class = WorkInterestSerializer
    filter_backends = [filters.SearchFilter, django_filters.DjangoFilterBackend]
    search_fields = ["title", "skills__name"]
    filterset_class = WorkInterestFilterSet

    def get_serializer_class(self):
        if self.request.method == "GET":
            return WorkInterestListSerializer
        return WorkInterestSerializer

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()


class WorkInterestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkInterest.objects.all()
    serializer_class = WorkInterestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return WorkInterestListSerializer
        return WorkInterestSerializer


class WorkInterestHireCreateView(generics.CreateAPIView):
    queryset = WorkInterestHire.objects.all()
    serializer_class = WorkInterestHireSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        work_interest_id = self.kwargs.get("pk")
        work_interest = get_object_or_404(WorkInterest, pk=work_interest_id)

        hire_request = serializer.save(work_interest=work_interest)

        # Send email notifications
        try:
            send_work_interest_hire_emails(hire_request)
        except Exception as e:
            # Log error but don't fail the request
            print(f"Failed to send hire request emails: {e}")
