from rest_framework import serializers

from accounts.models import CustomUser
from accounts.serializers import UserSerializerForJobSeeker

from .models import (
    CareerHistory,
    Certification,
    Company,
    Education,
    HireRequest,
    Industry,
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
)


class CompanySmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "company_name", "slug", "logo", "industry"]


class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
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


class CompanySerializer(serializers.ModelSerializer):
    user = UserSerializerForJobSeeker(read_only=True)
    industry = IndustrySerializer(read_only=True)
    logo = serializers.FileField(required=False)
    company_registration_certificate = serializers.FileField(required=False)
    established_date = serializers.DateField(required=False)
    website = serializers.URLField(required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model = Company
        fields = "__all__"
        read_only_fields = ("slug", "is_verified")

    def create(self, validated_data):
        industry_data = validated_data.pop("industry")
        industry = Industry.objects.get_or_create(**industry_data)[0]
        company = Company.objects.create(industry=industry, **validated_data)
        return company


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
    location = LocationSmallSerializer(many=True, read_only=True)
    unit_group = UnitGroupSmallSerializer(read_only=True)
    job_post_count = serializers.SerializerMethodField()
    total_applicant_count = serializers.SerializerMethodField()
    has_already_saved = serializers.SerializerMethodField()
    is_applied = serializers.SerializerMethodField()

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

    def get_job_post_count(self, obj):
        request = self.context.get("request")
        if request and hasattr(request, "user") and request.user.is_authenticated:
            try:
                company = Company.objects.get(user=request.user)
                return JobPost.objects.filter(company=company).count()
            except Company.DoesNotExist:
                return 0
        return 0

    def get_total_applicant_count(self, obj):
        request = self.context.get("request")
        if request and hasattr(request, "user") and request.user.is_authenticated:
            try:
                company = Company.objects.get(user=request.user)
                return JobApplication.objects.filter(job__company=company).count()
            except Company.DoesNotExist:
                return 0
        return 0

    def get_is_applied(self, obj):
        request = self.context.get("request")
        if request and hasattr(request, "user") and request.user.is_authenticated:
            try:
                _ = JobSeeker.objects.get(user=request.user)
                return JobApplication.objects.filter(
                    job=obj, applicant=request.user
                ).exists()
            except JobSeeker.DoesNotExist:
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
            "job_post_count",
            "is_applied",
        ]
        depth = 2


class JobPostListSerializer(serializers.ModelSerializer):
    location = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Location.objects.all(), required=False
    )
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
    company = CompanySerializer(read_only=True)
    location = LocationSerializer(many=True, read_only=True)
    unit_group = UnitGroupSerializer(read_only=True)
    applications_count = serializers.IntegerField(read_only=True)
    views_count = serializers.IntegerField(read_only=True)
    has_already_applied = serializers.SerializerMethodField()
    application_id = serializers.SerializerMethodField()

    def get_has_already_applied(self, obj):
        request = self.context.get("request")
        if request and hasattr(request, "user") and request.user.is_authenticated:
            try:
                _ = JobSeeker.objects.get(user=request.user)
                return JobApplication.objects.filter(
                    job=obj, applicant=request.user
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
    preferred_locations = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Location.objects.all(), required=False
    )
    preferred_unit_groups = serializers.PrimaryKeyRelatedField(
        many=True, queryset=UnitGroup.objects.all(), required=False
    )
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
    location = LocationSmallSerializer(many=True, read_only=True)
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
    already_hired = serializers.SerializerMethodField()

    def get_already_hired(self, obj):
        request = self.context.get("request")
        if (
            request
            and hasattr(request, "user")
            and request.user.user_type == "Employer"
        ):
            try:
                company = Company.objects.get(user=request.user)
                return HireRequest.objects.filter(
                    job__company=company, job_seeker=obj.user
                ).exists()
            except Company.DoesNotExist:
                return False
        return False

    class Meta:
        model = JobSeeker
        fields = "__all__"
        read_only_fields = ("slug",)
        depth = 2


class JobPostCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating job posts"""

    location = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Location.objects.all(), required=False
    )
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    unit_group = serializers.PrimaryKeyRelatedField(queryset=UnitGroup.objects.all())

    class Meta:
        model = JobPost
        fields = "__all__"
        read_only_fields = ["slug", "views_count", "applications_count"]


class UserSerializer(serializers.ModelSerializer):
    jobseeker_data = serializers.SerializerMethodField()
    company_data = serializers.SerializerMethodField()

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

    def get_company_data(self, obj):
        try:
            company = obj.company_profile
            return {
                "slug": company.slug,
            }
        except Company.DoesNotExist:
            return None
