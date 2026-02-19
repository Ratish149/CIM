from rest_framework import serializers

from accounts.models import CustomUser
from accounts.serializers import UserSerializerForJobSeeker

from .models import (
    ApprenticeshipApplication,
    ApprenticeshipDocument,
    CareerHistory,
    Certification,
    Education,
    HireRequest,
    Internship,
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


class InternshipIndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = InternshipIndustry
        fields = "__all__"
        read_only_fields = ("slug",)


class UnitGroupSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitGroup
        fields = ["id", "code", "title", "slug", "minor_group"]
        depth = 4


class MajorGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MajorGroup
        fields = ["id", "code", "title", "slug", "description"]


class SubMajorGroupSerializer(serializers.ModelSerializer):
    major_group = MajorGroupSerializer(read_only=True)

    class Meta:
        model = SubMajorGroup
        fields = ["id", "major_group", "code", "title", "slug", "description"]


class MinorGroupSerializer(serializers.ModelSerializer):
    sub_major_group = SubMajorGroupSerializer(read_only=True)

    class Meta:
        model = MinorGroup
        fields = ["id", "sub_major_group", "code", "title", "slug", "description"]


class UnitGroupSerializer(serializers.ModelSerializer):
    minor_group = MinorGroupSerializer(read_only=True)

    class Meta:
        model = UnitGroup
        fields = ["id", "minor_group", "code", "title", "slug", "description"]


class LocationSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["id", "name", "slug"]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
        read_only_fields = ("slug",)


class JobListAllSerializer(serializers.ModelSerializer):
    user = UserSerializerForJobSeeker(read_only=True)
    unit_group = UnitGroupSmallSerializer(read_only=True)
    total_applicant_count = serializers.SerializerMethodField()
    has_already_saved = serializers.SerializerMethodField()
    is_applied = serializers.SerializerMethodField()

    def get_has_already_saved(self, obj):
        # Check for annotated field first
        if hasattr(obj, "has_already_saved_annotated"):
            return obj.has_already_saved_annotated

        request = self.context.get("request")
        if request and hasattr(request, "user") and request.user.is_authenticated:
            try:
                # Use prefetch cache if available
                if hasattr(request.user, "saved_jobs_cache"):
                    return obj.id in request.user.saved_jobs_cache
                return SavedJob.objects.filter(
                    job=obj, job_seeker=request.user
                ).exists()
            except Exception:
                return False
        return False

    def get_total_applicant_count(self, obj):
        # Check for annotated field first
        if hasattr(obj, "total_applicant_count_annotated"):
            return obj.total_applicant_count_annotated

        return getattr(obj, "applications_count", 0)

    def get_is_applied(self, obj):
        # Check for annotated field first
        if hasattr(obj, "is_applied_annotated"):
            return obj.is_applied_annotated

        request = self.context.get("request")
        if request and hasattr(request, "user") and request.user.is_authenticated:
            try:
                # Use prefetch cache if available
                if hasattr(request.user, "applied_jobs_cache"):
                    return obj.id in request.user.applied_jobs_cache
                return JobApplication.objects.filter(
                    job=obj, applicant=request.user
                ).exists()
            except Exception:
                return False
        return False

    class Meta:
        model = JobPost
        fields = [
            "id",
            "title",
            "company_name",
            "user",
            "slug",
            "location",
            "status",
            "posted_date",
            "deadline",
            "employment_type",
            "applications_count",
            "views_count",
            "salary_range_min",
            "salary_range_max",
            "show_salary",
            "unit_group",
            "has_already_saved",
            "total_applicant_count",
            "is_applied",
        ]
        depth = 2


class JobPostListSerializer(serializers.ModelSerializer):
    applications_count = serializers.IntegerField(read_only=True)
    views_count = serializers.IntegerField(read_only=True)
    unit_group = UnitGroupSerializer(read_only=True)

    class Meta:
        model = JobPost
        fields = [
            "id",
            "user",
            "title",
            "company_name",
            "slug",
            "required_skill_level",
            "required_education",
            "salary_range_min",
            "salary_range_max",
            "location",
            "status",
            "posted_date",
            "deadline",
            "employment_type",
            "applications_count",
            "views_count",
            "show_salary",
            "description",
            "responsibilities",
            "requirements",
            "unit_group",
        ]
        read_only_fields = ["slug", "views_count", "applications_count"]


class JobPostDetailSerializer(serializers.ModelSerializer):
    unit_group = UnitGroupSerializer(read_only=True)
    applications_count = serializers.IntegerField(read_only=True)
    views_count = serializers.IntegerField(read_only=True)
    has_already_applied = serializers.SerializerMethodField()
    application_id = serializers.SerializerMethodField()

    def get_has_already_applied(self, obj):
        # Check for annotated field first
        if hasattr(obj, "has_already_applied_annotated"):
            return obj.has_already_applied_annotated

        request = self.context.get("request")
        if request and hasattr(request, "user") and request.user.is_authenticated:
            try:
                return JobApplication.objects.filter(
                    job=obj, applicant=request.user
                ).exists()
            except Exception:
                return False
        return False

    def get_application_id(self, obj):
        request = self.context.get("request")
        if request and hasattr(request, "user") and request.user.is_authenticated:
            try:
                _ = JobSeeker.objects.get(user=request.user)
                application = JobApplication.objects.filter(
                    job=obj, applicant=request.user
                ).first()
                return application.id if application else None
            except JobSeeker.DoesNotExist:
                return None
        return None

    class Meta:
        model = JobPost
        fields = "__all__"
        read_only_fields = ["slug", "views_count", "applications_count"]


class JobApplicationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating job applications"""

    class Meta:
        model = JobApplication
        fields = ["job", "cover_letter"]

    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["applicant"] = request.user
        return super().create(validated_data)


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = "__all__"


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = "__all__"


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"

    def to_internal_value(self, data):
        print(f"EducationSerializer received: {data}")
        try:
            result = super().to_internal_value(data)
            print(f"EducationSerializer validated: {result}")
            return result
        except Exception as e:
            print(f"EducationSerializer validation error: {e}")
            raise


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class CareerHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerHistory
        fields = "__all__"


class JobSeekerSerializer(serializers.ModelSerializer):
    user = UserSerializerForJobSeeker(read_only=True)
    education = EducationSerializer(many=True, required=False)
    certifications = CertificationSerializer(many=True, required=False)
    languages = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Language.objects.all(), required=False
    )
    skills = SkillSerializer(many=True, required=False)

    career_histories = CareerHistorySerializer(many=True, required=False)

    class Meta:
        model = JobSeeker
        fields = "__all__"
        read_only_fields = ("slug",)
        depth = 2

    def create(self, validated_data):
        education_data = validated_data.pop("education", [])
        certifications_data = validated_data.pop("certifications", [])
        career_histories_data = validated_data.pop("career_histories", [])

        job_seeker = JobSeeker.objects.create(**validated_data)

        if education_data:
            for edu_data in education_data:
                education = Education.objects.create(**edu_data)
                job_seeker.education.add(education)

        if certifications_data:
            for cert_data in certifications_data:
                certification = Certification.objects.create(**cert_data)
                job_seeker.certifications.add(certification)

        if career_histories_data:
            for career_history_data in career_histories_data:
                career_history = CareerHistory.objects.create(**career_history_data)
                job_seeker.career_history.add(career_history)

        return job_seeker


class JobApplicationSerializer(serializers.ModelSerializer):
    job = JobListAllSerializer(read_only=True)

    class Meta:
        model = JobApplication
        fields = "__all__"
        read_only_fields = ["applied_date", "updated_at", "status", "applicant"]


class JobApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ["status"]


class SavedJobCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating saved jobs"""

    class Meta:
        model = SavedJob
        fields = ["job"]

    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["job_seeker"] = request.user
        return super().create(validated_data)


class SavedJobSerializer(serializers.ModelSerializer):
    job = JobListAllSerializer(read_only=True)

    class Meta:
        model = SavedJob
        fields = "__all__"
        read_only_fields = ["saved_date"]


class HireRequestStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HireRequest
        fields = ["status"]


class HireJobPostListSerializer(serializers.ModelSerializer):
    application_id = serializers.SerializerMethodField()
    # location is now a CharField in model, handled automatically
    unit_group = UnitGroupSmallSerializer(read_only=True)
    has_already_saved = serializers.SerializerMethodField()

    def get_has_already_saved(self, obj):
        request = self.context.get("request")
        if request and hasattr(request, "user") and request.user.is_authenticated:
            try:
                _ = JobSeeker.objects.get(user=request.user)
                return SavedJob.objects.filter(
                    job=obj, job_seeker=request.user
                ).exists()
            except JobSeeker.DoesNotExist:
                return False
        return False

    def get_application_id(self, obj):
        request = self.context.get("request")
        if request and hasattr(request, "user") and request.user.is_authenticated:
            try:
                _ = JobSeeker.objects.get(user=request.user)
                application = JobApplication.objects.filter(
                    job=obj, applicant=request.user
                ).first()
                return application.id if application else None
            except JobSeeker.DoesNotExist:
                return None
        return None

    class Meta:
        model = JobPost
        fields = [
            "id",
            "title",
            "slug",
            "location",
            "status",
            "posted_date",
            "deadline",
            "employment_type",
            "salary_range_min",
            "salary_range_max",
            "show_salary",
            "unit_group",
            "has_already_saved",
            "application_id",
        ]
        depth = 2


class HireRequestSerializer(serializers.ModelSerializer):
    job = HireJobPostListSerializer(read_only=True)
    job_seeker = JobSeekerSerializer(read_only=True)

    class Meta:
        model = HireRequest
        fields = [
            "id",
            "job",
            "job_seeker",
            "requested_date",
            "status",
            "message",
            "seeker_message",
        ]
        read_only_fields = ["requested_date"]


class ImportGroupsSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.endswith(".csv"):
            raise serializers.ValidationError("File must be a CSV.")
        return value


class JobSeekerSerializer2(serializers.ModelSerializer):
    user = UserSerializerForJobSeeker(read_only=True)
    education = EducationSerializer(many=True, required=False)
    certifications = CertificationSerializer(many=True, required=False)
    languages = LanguageSerializer(many=True, required=False)
    skills = SkillSerializer(many=True, required=False)
    preferred_locations = LocationSerializer(many=True, required=False)
    career_histories = CareerHistorySerializer(many=True, required=False)

    class Meta:
        model = JobSeeker
        fields = "__all__"
        read_only_fields = ("slug",)
        depth = 2


class JobPostCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating job posts"""

    # location handles as CharField from model
    unit_group = serializers.PrimaryKeyRelatedField(queryset=UnitGroup.objects.all())

    class Meta:
        model = JobPost
        fields = "__all__"
        read_only_fields = ["slug", "views_count", "applications_count"]


class UserSerializer(serializers.ModelSerializer):
    jobseeker_data = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "user_type",
            "gender",
            "phone_number",
            "address",
            "jobseeker_data",
            "company_data",
        )
        read_only_fields = ("id",)

    def get_jobseeker_data(self, obj):
        try:
            jobseeker = obj.jobseeker
            return {
                "slug": jobseeker.slug,
            }
        except JobSeeker.DoesNotExist:
            return None


class InternshipRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for internship registration that handles education and documents.
    """

    # Special fields handled manually
    education = serializers.ListField(
        child=serializers.DictField(), required=False, write_only=True
    )
    documents = serializers.ListField(required=False, write_only=True)

    class Meta:
        model = Internship
        fields = [
            "id",
            "full_name",
            "permanent_district",
            "permanent_municipality",
            "permanent_province",
            "permanent_ward",
            "current_district",
            "current_municipality",
            "current_province",
            "current_ward",
            "contact_number",
            "email",
            "date_of_birth",
            "motivational_letter",
            "supervisor_name",
            "supervisor_email",
            "supervisor_phone",
            "internship_industry",
            "preferred_department",
            "internship_duration",
            "internship_month",
            "preferred_start_date",
            "availability",
            "education",
            "documents",
        ]

    def to_internal_value(self, data):
        """Parse JSON strings for education data."""
        import json

        # Convert QueryDict to dict
        if hasattr(data, "dict"):
            new_data = {}
            for key in data.keys():
                if key == "documents":
                    new_data[key] = data.getlist(key)
                elif key == "education":
                    # Get the value (might be JSON string)
                    value = data.get(key)
                    if isinstance(value, str) and value.strip():
                        try:
                            new_data["education"] = json.loads(value)
                        except (ValueError, TypeError):
                            new_data["education"] = []
                    else:
                        new_data["education"] = []
                else:
                    new_data[key] = data.get(key)
            data = new_data

        # Parse education if it's a JSON string
        if "education" in data and isinstance(data["education"], str):
            try:
                data["education"] = json.loads(data["education"])
            except (ValueError, TypeError):
                data["education"] = []

        return super().to_internal_value(data)

    def create(self, validated_data):
        """Create Internship seekr with education and documents."""
        request = self.context.get("request")

        # Extract education and documents
        education_list = validated_data.pop("education", [])
        documents = validated_data.pop("documents", [])

        # Get documents from request.FILES if not in validated_data
        if not documents and request and request.FILES:
            documents = request.FILES.getlist("documents")

        # Determine user
        user = request.user if request and request.user.is_authenticated else None

        # Create or update Internship seeker
        if user:
            internship_seeker, created = Internship.objects.update_or_create(
                user=user, defaults=validated_data
            )
        else:
            internship_seeker = Internship.objects.create(user=None, **validated_data)

        # Create and add education records
        for edu_data in education_list:
            try:
                education = Education.objects.create(
                    institution=edu_data.get("institution", ""),
                    course_or_qualification=edu_data.get(
                        "course_or_qualification", "No Education"
                    ),
                    year_of_completion=edu_data.get("year_of_completion"),
                    course_highlights=edu_data.get("course_highlights", ""),
                )
                internship_seeker.education.add(education)
            except Exception as e:
                print(f"Error creating education: {e}")

        # Create and add documents as certifications
        for doc_file in documents:
            if hasattr(doc_file, "name"):
                try:
                    certification = Certification.objects.create(
                        name=doc_file.name,
                        issuing_organisation="Internship Document",
                        image=doc_file,
                    )
                    internship_seeker.certifications.add(certification)
                except Exception as e:
                    print(f"Error creating certification: {e}")

        return internship_seeker


class ApprenticeshipDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprenticeshipDocument
        fields = ["id", "document", "name", "uploaded_at"]


class ApprenticeshipApplicationSerializer(serializers.ModelSerializer):
    documents = serializers.ListField(
        child=serializers.FileField(), required=False, write_only=True
    )
    uploaded_documents = ApprenticeshipDocumentSerializer(
        source="documents", many=True, read_only=True
    )

    class Meta:
        model = ApprenticeshipApplication
        fields = "__all__"

    def to_internal_value(self, data):
        """Parse QueryDict to handle documents list correctly."""
        if hasattr(data, "dict"):
            new_data = {}
            for key in data.keys():
                if key == "documents":
                    # Important: getlist to retrieve all files
                    new_data[key] = data.getlist(key)
                else:
                    new_data[key] = data.get(key)
            data = new_data

        return super().to_internal_value(data)

    def create(self, validated_data):
        request = self.context.get("request")

        # Extract documents
        documents_data = validated_data.pop("documents", [])

        # Get documents from request.FILES if not in validated_data
        if not documents_data and request and request.FILES:
            documents_data = request.FILES.getlist("documents")

        application = ApprenticeshipApplication.objects.create(**validated_data)

        for doc in documents_data:
            if hasattr(doc, "name"):
                ApprenticeshipDocument.objects.create(
                    application=application, document=doc, name=doc.name
                )

        return application


class WorkInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkInterest
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at", "user")


class WorkInterestListSerializer(serializers.ModelSerializer):
    unit_group = UnitGroupSmallSerializer(read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    user = UserSerializerForJobSeeker(read_only=True)

    class Meta:
        model = WorkInterest
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at", "user")


class WorkInterestHireSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkInterestHire
        fields = [
            "id",
            "work_interest",
            "name",
            "email",
            "phone",
            "message",
            "created_at",
        ]
        read_only_fields = ["created_at"]

    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user") and request.user.is_authenticated:
            validated_data["user"] = request.user
        return super().create(validated_data)
