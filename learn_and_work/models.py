from django.db import models


class LearnAndWorkBooking(models.Model):
    """
    Stores group training session booking requests submitted from the
    Learn and Work Platform page at Birat Expo 2026 (17–26 December).

    One booking = one group (15–20 students) in one zone on one day at one session.

    Zones (10):
        Career Planning | CIM Member Space | Health & Emergency Care |
        Industry & Automation | ICT & Smart Technology | Beauty & Wellness |
        Agriculture & Urban Farming | Fashion & Textile |
        Hospitality & Tourism | Security & Surveillance

    Sessions (3 per day):
        A: 9:30 AM – 11:30 AM
        B: 12:00 PM – 2:00 PM
        C: 3:00 PM – 5:00 PM

    Days: 17–26 December 2026 (10 days)
    """

    # ── Session details ───────────────────────────────────────────────────────
    # e.g. "Career Planning"
    zone = models.CharField(max_length=100, db_index=True)

    # e.g. "17 December 2026"
    date = models.CharField(max_length=50, db_index=True)

    # e.g. "9:30 AM – 11:30 AM"
    time = models.CharField(max_length=50)

    # ── Group / School details ─────────────────────────────────────────────────
    school = models.CharField(max_length=255)  # School or group name
    grade = models.CharField(max_length=100)  # Class or grade, e.g. "Grade 9"
    teacher = models.CharField(max_length=255)  # Teacher or contact person
    phone = models.CharField(max_length=20, db_index=True)
    email = models.CharField(max_length=255, blank=True)

    # Number of students (15–20), stored as text to match frontend
    students = models.CharField(max_length=5)

    # Anything they should know (accessibility, arrival time, etc.)
    note = models.TextField(blank=True)

    # ── Timestamps ────────────────────────────────────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Learn & Work Booking"
        verbose_name_plural = "Learn & Work Bookings"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["zone", "date", "time"]),
            models.Index(fields=["phone"]),
        ]

    def __str__(self):
        return f"{self.zone} | {self.date} {self.time} | {self.school} ({self.teacher})"
