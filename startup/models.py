from django.db import models

from startup.constants import HeardAboutUs, RegistrationStatus, TrackType


class StartUpRegistration(models.Model):
    """
    Model for BIC Pavilion enquiry registrations at Birat Expo 2026.
    Similar values across tracks (name, phone, email, municipality, organization, role, notes)
    are consolidated into unified fields, while track-specific fields have full descriptive names.
    """

    # =========================================================================
    # Common Meta & Status
    # =========================================================================
    track = models.CharField(
        max_length=30,
        choices=TrackType.choices,
        db_index=True,
        verbose_name="Track / Room",
        help_text="Makerspace, Design Studio, or Growth Room",
    )
    status = models.CharField(
        max_length=20,
        choices=RegistrationStatus.choices,
        default=RegistrationStatus.PENDING,
        db_index=True,
        verbose_name="Status",
    )
    heard_about_us = models.CharField(
        max_length=100,
        choices=HeardAboutUs.choices,
        blank=True,
        null=True,
        verbose_name="How did you hear about us?",
    )
    consent = models.BooleanField(
        default=False,
        verbose_name="Consent to be contacted",
        help_text="Agreed to allow Biratnagar Incubation Center / CIM to contact regarding this enquiry",
    )
    keep_updated = models.BooleanField(
        default=False,
        verbose_name="Keep updated about other programmes",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="Submitted At",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Last Updated At",
    )

    # =========================================================================
    # Consolidated Contact & Location Details (Single field for similar values)
    # =========================================================================
    full_name = models.CharField(
        max_length=255,
        verbose_name="Full Name",
        help_text="Applicant / Contact person full name",
    )
    phone = models.CharField(
        max_length=30,
        verbose_name="Mobile / Phone Number",
        help_text="Contact telephone / mobile number",
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Email Address",
    )
    organization_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="School / College / Business Name",
        help_text="School name, college name, or enterprise / company name",
    )
    role = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Role / Designation",
        help_text="e.g. Principal, Teacher, Student, Owner / Founder, Manager",
    )
    municipality = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Municipality / Location",
        help_text="e.g. Biratnagar, Morang / Itahari, Sunsari",
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Notes / Queries",
        help_text="Single notes field for all user queries, accessibility needs, or additional comments",
    )

    # =========================================================================
    # ROOM 1 · MAKERSPACE (Schools & Teachers) Details
    # =========================================================================
    school_request = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="School Request Type",
        help_text="e.g. 'Class visit to Room 1 at Birat Expo' or 'Maker session at our school'",
    )
    school_type = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="School Type",
        help_text="e.g. Community (government), Institutional (private), Other",
    )
    school_grades = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Grades Taking Part",
        help_text="Comma-separated grade levels (e.g., '7, 8, 9, 10')",
    )
    school_students_count = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Number of Students",
    )
    school_teachers_count = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Teachers Accompanying",
    )
    school_preferred_date_1 = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Visit First-choice Date",
    )
    school_preferred_date_2 = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Visit Second-choice Date",
    )
    school_session_slot = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Preferred Session Slot",
        help_text="e.g. Morning, Afternoon, Either",
    )
    school_session_month = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Preferred Month for Onsite Session",
        help_text="e.g. Magh 2083, Falgun 2083, Flexible",
    )
    school_available_space = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Available Space at School",
        help_text="e.g. Classroom, Hall / multipurpose room, Computer lab",
    )

    # =========================================================================
    # ROOM 2 · DESIGN STUDIO (College Students) Details
    # =========================================================================
    gender = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Gender",
    )
    age_group = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Age Group",
        help_text="e.g. Under 18, 18–21, 22–25, 26–30, Over 30",
    )
    college_programme = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Faculty / Programme",
        help_text="e.g., BBS, BBA, BSc CSIT, BE",
    )
    college_year = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Year / Semester",
        help_text="e.g. 1st year, 2nd year, 3rd year, 4th year, Master's, Recently graduated",
    )
    idea_stage = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Idea Stage",
        help_text="e.g. No idea yet, just curious / I have a rough idea / Already working on something",
    )
    interested_topics = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Interested Topics",
        help_text="Comma-separated topics (e.g., 'Agriculture & food, Tech & digital')",
    )
    preferred_contact_channel = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Preferred Contact Channel",
        help_text="e.g. Phone call, SMS, Viber / WhatsApp, Email",
    )
    willing_to_host_workshop = models.BooleanField(
        default=False,
        verbose_name="Interested in hosting workshop at college",
    )

    # =========================================================================
    # ROOM 3 · GROWTH ROOM (Business Owners) Details
    # =========================================================================
    district = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="District",
        help_text="District in Koshi Province or Outside Koshi Province",
    )
    business_registration_type = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Registration Type",
        help_text="e.g. Company (OCR), Cottage & Small Industries (DoCSI), Municipality / ward, Cooperative, Not registered yet",
    )
    trading_duration = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Time Trading",
        help_text="e.g. Less than 1 year, 1–3 years, 3–5 years, 5–10 years, More than 10 years",
    )
    business_sector = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Business Sector",
        help_text="e.g. Agriculture & agro-processing, Manufacturing, Tourism & hospitality, IT & digital",
    )
    employees_count = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="People Employed",
        help_text="e.g. 1–4, 5–9, 10–19, 20–49, 50+",
    )
    annual_turnover = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Annual Turnover",
        help_text="e.g. Below NPR 10 lakh, NPR 10–50 lakh, NPR 1–5 crore",
    )
    ownership_diversity = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Ownership Diversity",
        help_text="Comma-separated attributes (e.g., 'Women-led, Youth-led (under 40)')",
    )
    area_of_interest = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Area of Interest",
        help_text="e.g. Health Check-up + SGB Accelerator, Health Check-up only, SGB Accelerator only",
    )
    expo_visit_day = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Preferred Day for Room 3 Visit",
    )
    support_needs = models.TextField(
        blank=True,
        null=True,
        verbose_name="Support Needs",
        help_text="Comma-separated selected support areas",
    )
    biggest_challenge = models.TextField(
        blank=True,
        null=True,
        verbose_name="Biggest Business Challenge",
    )

    class Meta:
        db_table = "startup_registrations"
        verbose_name = "BIC Pavilion Enquiry"
        verbose_name_plural = "BIC Pavilion Enquiries"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["track", "status"]),
            models.Index(fields=["created_at", "status"]),
            models.Index(fields=["phone"]),
            models.Index(fields=["email"]),
        ]

    def __str__(self) -> str:
        return f"[{self.id}] {self.full_name} ({self.organization_name or self.get_track_display()})"
