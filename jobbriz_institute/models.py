from django.db import models


# Create your models here.
class Institute(models.Model):
    INSTITUTE_TYPE_CHOICES = (
        ("Technical School", "Technical School"),
        ("Polytechnic", "Polytechnic"),
        ("Training Centre", "Training Centre"),
        ("College", "College"),
    )
    institute_name = models.CharField(max_length=100)
    institute_type = models.CharField(max_length=100, choices=INSTITUTE_TYPE_CHOICES)
    province = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    municipality = models.CharField(max_length=100)
    ward_no = models.IntegerField()
    phone_number = models.CharField(max_length=15)
    website = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField()
    logo = models.ImageField(upload_to="institute_logos/", null=True, blank=True)
    primary_contact_person = models.CharField(max_length=100)
    primary_contact_person_phone = models.CharField(max_length=15)
    primary_contact_person_email = models.EmailField()
    primary_contact_person_designation = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.institute_name


class GraduateRoster(models.Model):
    LEVEL_COMPLETED_CHOICES = (
        ("Pre-Diploma", "Pre-Diploma"),
        ("Diploma", "Diploma"),
        ("TSLC", "TSLC"),
        ("Short Course", "Short Course"),
        ("Bachelor", "Bachelor"),
        ("Other", "Other"),
    )
    CERTIFYING_AGENCY_CHOICES = (
        ("CTEVT", "CTEVT"),
        ("University", "University"),
        ("Other", "Other"),
    )
    JOB_STATUS_CHOICES = (
        ("Available for Job", "Available for Job"),
        ("Not Available", "Not Available"),
    )

    institute = models.ForeignKey(
        Institute, on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()

    permanent_province = models.CharField(max_length=255)
    permanent_district = models.CharField(max_length=255)
    permanent_municipality = models.CharField(max_length=255)
    permanent_ward = models.CharField(max_length=255)

    current_province = models.CharField(max_length=255, null=True, blank=True)
    current_district = models.CharField(max_length=255, null=True, blank=True)
    current_municipality = models.CharField(max_length=255, null=True, blank=True)
    current_ward = models.CharField(max_length=255, null=True, blank=True)

    level_completed = models.CharField(
        max_length=50, choices=LEVEL_COMPLETED_CHOICES, null=True, blank=True
    )
    subject_trade_stream = models.CharField(max_length=100, null=True, blank=True)
    specialization_key_skills = models.TextField(null=True, blank=True)
    passed_year = models.IntegerField(null=True, blank=True)
    certifying_agency = models.CharField(
        max_length=100, choices=CERTIFYING_AGENCY_CHOICES, null=True, blank=True
    )
    certifying_agency_name = models.CharField(
        max_length=255, null=True, blank=True, help_text="Write the Name if Other"
    )
    certificate_id = models.CharField(max_length=100, null=True, blank=True)
    job_status = models.CharField(
        max_length=50, choices=JOB_STATUS_CHOICES, default="Available for Job"
    )
    available_from = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
