from django.db import models


class BDSConnect(models.Model):
    """
    Stores registrations from the BIRATBAZAAR BDS Connect Pavilion form.
    Covers both the 'Business' track and the 'Service Provider' track.
    """

    # ── Track choices (only this field uses choices) ──────────────────────────
    TRACK_BUSINESS = "business"
    TRACK_PROVIDER = "provider"
    TRACK_CHOICES = [
        (TRACK_BUSINESS, "Business"),
        (TRACK_PROVIDER, "Service Provider"),
    ]
    track = models.CharField(max_length=20, choices=TRACK_CHOICES)

    # ── About you (shared) ────────────────────────────────────────────────────
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=50, blank=True)

    # ── Business / Organisation name (shared between both tracks) ─────────────
    business_name = models.CharField(max_length=255, blank=True)
    district = models.CharField(max_length=100, blank=True)
    web = models.CharField(max_length=255, blank=True)

    # ── BUSINESS TRACK ────────────────────────────────────────────────────────

    # What would you like to do? (semicolon-separated checkbox values)
    want = models.CharField(max_length=500, blank=True)

    sector = models.CharField(max_length=100, blank=True)
    registered = models.CharField(max_length=50, blank=True)
    years = models.CharField(max_length=50, blank=True)
    staff = models.CharField(max_length=50, blank=True)

    # Is the business led by… (semicolon-separated checkbox values)
    ledby = models.CharField(max_length=255, blank=True)

    # Where do you need help? (semicolon-separated checkbox values)
    needs = models.CharField(max_length=1000, blank=True)

    # Biggest problem your business faces right now
    problem = models.TextField(blank=True)

    # Your visit
    day = models.CharField(max_length=50, blank=True)
    time = models.CharField(max_length=50, blank=True)

    # ── SERVICE PROVIDER TRACK ────────────────────────────────────────────────

    # Services you offer (semicolon-separated checkbox values)
    services = models.CharField(max_length=1000, blank=True)

    # Describe your service in a few lines
    description = models.TextField(blank=True)

    # How would you like to take part? (semicolon-separated checkbox values)
    participation = models.CharField(max_length=500, blank=True)

    # ── Timestamps ────────────────────────────────────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "BDS Connect Registration"
        verbose_name_plural = "BDS Connect Registrations"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["track", "created_at"]),
            models.Index(fields=["phone"]),
        ]

    def __str__(self):
        return f"[{self.get_track_display()}] {self.name} – {self.business_name}"


class BDSCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Tags(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class BDSService(models.Model):
    FINANCE_CHOICES = [
        ("Meet your VCs", "Meet your VCs"),
        ("Meet your Banks", "Meet your Banks"),
    ]
    Company_name = models.CharField(max_length=255)
    finance_services = models.CharField(
        max_length=255, choices=FINANCE_CHOICES, null=True, blank=True
    )
    service = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(BDSCategory, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tags)
    logo = models.FileField(upload_to="bds_service_logos/", blank=True, null=True)

    def __str__(self):
        return f"{self.Company_name} - {self.service}"
