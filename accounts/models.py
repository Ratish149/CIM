from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    DESIGNATION_CHOICES = [
        ("CEO", "Chief Executive Officer"),
        ("CFO", "Chief Financial Officer"),
        ("CTO", "Chief Technology Officer"),
        ("CMO", "Chief Marketing Officer"),
        ("COO", "Chief Operating Officer"),
        ("CIO", "Chief Information Officer"),
        ("CSO", "Chief Security Officer"),
        ("Other", "Other"),
    ]
    USER_TYPE_CHOICES = [
        ("Employer", "Employer"),
        ("Job Seeker", "Job Seeker"),
        ("Wisher", "Wisher"),
        ("Offerer", "Offerer"),
    ]
    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]

    user_type = models.CharField(
        max_length=10, choices=USER_TYPE_CHOICES, null=True, blank=True
    )
    gender = models.CharField(
        max_length=6, choices=GENDER_CHOICES, null=True, blank=True
    )
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    avatar = models.FileField(upload_to="avatar/", null=True, blank=True)
    designation = models.CharField(
        max_length=100, choices=DESIGNATION_CHOICES, default="Other"
    )
    has_institute = models.BooleanField(default=False)
    alternate_no = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.email


class Organization(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="organizations"
    )
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    country = models.CharField(max_length=100, default="Nepal")
    province_state = models.CharField(max_length=100, default="Province 1")
    municipality_ward = models.CharField(max_length=100, default="Biratnagar")
    logo = models.FileField(upload_to="organization_logos/", blank=True)

    def __str__(self):
        return self.name


class File(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="files",
        blank=True,
        null=True,
    )
    file = models.FileField(upload_to="organization_files/")
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PasswordResetCode(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="password_reset_codes",
    )
    code = models.CharField(max_length=6, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(db_index=True)
    is_used = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "code", "is_used"]),
            models.Index(fields=["expires_at", "is_used"]),
        ]

    def is_valid(self) -> bool:
        return not self.is_used and timezone.now() <= self.expires_at

    def __str__(self):
        return f"Reset code for {self.user.email} (used={self.is_used})"
