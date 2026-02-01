from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from accounts.models import CustomUser


class SlugMixin:
    def generate_unique_slug(self):
        base_slug = slugify(self.title)
        slug = base_slug
        counter = 1
        model = self.__class__
        while model.objects.filter(slug=slug).exclude(id=self.id).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        self.slug = slug

    def save(self, *args, **kwargs):
        self.generate_unique_slug()
        super().save(*args, **kwargs)


class MajorGroup(SlugMixin, models.Model):
    """ISCO Major Group (1-digit code)"""

    code = models.CharField(max_length=1, unique=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.code} - {self.title}"


class SubMajorGroup(SlugMixin, models.Model):
    """ISCO Sub-Major Group (2-digit code)"""

    major_group = models.ForeignKey(
        MajorGroup, on_delete=models.CASCADE, related_name="sub_major_groups"
    )
    code = models.CharField(max_length=2, unique=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.code} - {self.title}"


class MinorGroup(SlugMixin, models.Model):
    """ISCO Minor Group (3-digit code)"""

    sub_major_group = models.ForeignKey(
        SubMajorGroup, on_delete=models.CASCADE, related_name="minor_groups"
    )
    code = models.CharField(max_length=3, unique=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.code} - {self.title}"


class UnitGroup(SlugMixin, models.Model):
    """ISCO Unit Group (4-digit code)"""

    minor_group = models.ForeignKey(
        MinorGroup, on_delete=models.CASCADE, related_name="unit_groups"
    )
    code = models.CharField(max_length=4, unique=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.code} - {self.title}"


class JobPost(SlugMixin, models.Model):
    STATUS_CHOICES = [
        ("Draft", "Draft"),
        ("Published", "Published"),
        ("Expired", "Expired"),
        ("Closed", "Closed"),
    ]

    EDUCATION_CHOICES = [
        ("General Literate", "General Literate"),
        ("Below SLC", "Below SLC"),
        ("+2", "+2"),
        ("Bachelors", "Bachelors"),
        ("Master & above", "Master & above"),
        ("Pre-Diploma", "Pre-Diploma"),
        ("Diploma", "Diploma"),
        ("TLSC", "TLSC"),
        ("No Education", "No Education"),
    ]

    LEVEL_CHOICES = [
        ("RPL", "RPL"),
        ("Level 1", "Level 1"),
        ("Level 2", "Level 2"),
        ("Level 3", "Level 3"),
        ("Level 4", "Level 4"),
        ("Level 5", "Level 5"),
        ("Level 6", "Level 6"),
        ("Level 7", "Level 7"),
        ("Level 8", "Level 8"),
        ("None", "None"),
    ]

    EMPLOYMENT_TYPE_CHOICES = [
        ("Full Time", "Full Time"),
        ("Part Time", "Part Time"),
        ("Contract", "Contract"),
        ("Internship", "Internship"),
        ("All", "All"),
    ]

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="job_posts",
        blank=True,
        null=True,
    )

    company = models.ForeignKey(
        "jobbriz.Company", on_delete=models.CASCADE, blank=True, null=True
    )
    company_name = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    unit_group = models.ForeignKey(UnitGroup, on_delete=models.CASCADE)
    required_skill_level = models.CharField(
        max_length=10, choices=LEVEL_CHOICES, default="None"
    )
    required_education = models.CharField(
        max_length=20, choices=EDUCATION_CHOICES, default="No Education"
    )
    description = models.TextField()
    responsibilities = models.TextField(blank=True, null=True)
    show_salary = models.BooleanField(default=True)
    requirements = models.TextField(blank=True, null=True)
    salary_range_min = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    salary_range_max = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    location = models.ManyToManyField("Location", related_name="job_posts")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Published"
    )
    posted_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES)
    views_count = models.PositiveIntegerField(default=0, blank=True)
    applications_count = models.PositiveIntegerField(default=0, blank=True)

    def __str__(self):
        return f"{self.title} at {self.company_name}"


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Reviewed", "Reviewed"),
        ("Shortlisted", "Shortlisted"),
        ("Rejected", "Rejected"),
        ("Hired", "Hired"),
    ]

    job = models.ForeignKey(
        JobPost, on_delete=models.CASCADE, related_name="applications"
    )
    applicant = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True
    )
    applied_date = models.DateTimeField(auto_now_add=True)
    cover_letter = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("job", "applicant")

    def __str__(self):
        return f"Application for {self.job.title} by {self.applicant.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class HireRequest(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Accepted", "Accepted"),
        ("Rejected", "Rejected"),
    ]

    job = models.ForeignKey(
        JobPost, on_delete=models.CASCADE, related_name="hire_requests"
    )
    job_seeker = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="hire_requests"
    )
    requested_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    message = models.TextField(blank=True, null=True)
    seeker_message = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ("job", "job_seeker")


class SavedJob(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name="saved_by")
    job_seeker = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="saved_jobs"
    )
    saved_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("job", "job_seeker")

    def __str__(self):
        return f"Saved job {self.job.title} by {self.job_seeker.username}"


class Skill(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Certification(models.Model):
    name = models.CharField(max_length=200)
    issuing_organisation = models.CharField(max_length=200)
    issue_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    image = models.FileField(upload_to="certifications/", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["issue_date"]


class Education(models.Model):
    COURSE_OR_QUALIFICATION_CHOICES = [
        ("General Literate", "General Literate"),
        ("Below SLC", "Below SLC"),
        ("+2", "+2"),
        ("Bachelors", "Bachelors"),
        ("Master & above", "Master & above"),
        ("Pre-Diploma", "Pre-Diploma"),
        ("Diploma", "Diploma"),
        ("TLSC", "TLSC"),
        ("No Education", "No Education"),
    ]

    course_or_qualification = models.CharField(
        max_length=50, choices=COURSE_OR_QUALIFICATION_CHOICES
    )
    institution = models.CharField(max_length=50)
    year_of_completion = models.DateField(blank=True, null=True)
    course_highlights = models.TextField(blank=True)

    def __str__(self):
        return self.course_or_qualification

    class Meta:
        ordering = ["year_of_completion"]


class Location(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            # Check if slug exists and generate a unique one
            while Location.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CareerHistory(models.Model):
    company_name = models.CharField(max_length=50)
    job_title = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.job_title

    class Meta:
        ordering = ["start_date"]


class JobSeeker(models.Model):
    LEVEL_CHOICES = [
        ("RPL", "RPL"),
        ("Level 1", "Level 1"),
        ("Level 2", "Level 2"),
        ("Level 3", "Level 3"),
        ("Level 4", "Level 4"),
        ("Level 5", "Level 5"),
        ("Level 6", "Level 6"),
        ("Level 7", "Level 7"),
        ("Level 8", "Level 8"),
        ("None", "None"),
    ]

    AVAILABILITY_CHOICES = [
        ("Full Time", "Full Time"),
        ("Part Time", "Part Time"),
        ("Contract", "Contract"),
        ("Internship", "Internship"),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    cv = models.FileField(upload_to="cvs/", blank=True, null=True)
    skill_levels = models.CharField(
        max_length=200, choices=LEVEL_CHOICES, default="None", blank=True, null=True
    )
    education = models.ManyToManyField(Education, blank=True)
    career_history = models.ManyToManyField(
        CareerHistory, blank=True, related_name="job_seeker_career_history"
    )
    preferred_unit_groups = models.ManyToManyField(
        "jobbriz.UnitGroup", blank=True, related_name="job_seeker_preferred_unit_groups"
    )
    work_experience = models.CharField(max_length=200, blank=True, null=True)
    skills = models.ManyToManyField(Skill, blank=True, related_name="job_seeker_skills")
    preferred_locations = models.ManyToManyField(
        Location, blank=True, related_name="job_seeker_preferred_locations"
    )
    preferred_salary_range_from = models.IntegerField(default=0, blank=True, null=True)
    preferred_salary_range_to = models.IntegerField(default=0, blank=True, null=True)
    remote_work_preference = models.BooleanField(default=False, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    availability = models.CharField(
        max_length=50,
        choices=AVAILABILITY_CHOICES,
        default="Full Time",
        blank=True,
        null=True,
    )
    certifications = models.ManyToManyField(
        Certification, blank=True, related_name="job_seeker_certifications"
    )
    languages = models.ManyToManyField(
        Language, blank=True, related_name="job_seeker_languages"
    )
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return f"Job Seeker - {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.user.username)
            slug = base_slug
            counter = 1
            # Check if slug exists and generate a unique one
            while JobSeeker.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Industry(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Industries"


class Company(models.Model):
    COMPANY_SIZE_CHOICES = [
        ("1-10", "1-10 employees"),
        ("11-50", "11-50 employees"),
        ("51-200", "51-200 employees"),
        ("201-500", "201-500 employees"),
        ("501-1000", "501-1000 employees"),
        ("1001+", "1001+ employees"),
    ]

    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="company_profile"
    )
    company_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE)
    company_size = models.CharField(max_length=20, choices=COMPANY_SIZE_CHOICES)
    registration_number = models.CharField(
        max_length=50, unique=True, blank=True, null=True
    )
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    logo = models.FileField(upload_to="company_logos/", null=True, blank=True)
    established_date = models.DateField(null=True, blank=True)
    company_email = models.EmailField(null=True, blank=True)
    company_registration_certificate = models.FileField(
        upload_to="company_registration_certificates/", null=True, blank=True
    )
    is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")
        ordering = ["company_name"]

    def save(self, *args, **kwargs):
        base_slug = slugify(self.company_name)
        if not self.slug or base_slug != slugify(
            Company.objects.get(pk=self.pk).company_name if self.pk else ""
        ):
            slug = base_slug
            counter = 1
            # Check if slug exists and generate a unique one
            while Company.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.company_name
