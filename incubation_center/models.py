from django.db import models


# Create your models here.
class IncubationCenter(models.Model):
    ROOM_CATEGORY = (
        ("The Big Brain Room", "The Big Brain Room"),
        ("The Grind Garage", "The Grind Garage"),
        ("The Fusion Lab", "The Fusion Lab"),
    )
    BOOKING_CHOICE = (
        ("Co-working Seat", "Co-working Seat"),
        ("Private Room", "Private Room"),
    )
    booking_type = models.CharField(max_length=100, choices=BOOKING_CHOICE)

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)

    name = models.CharField(max_length=100)
    founder_name = models.CharField(max_length=255, null=True, blank=True)
    founder_designation = models.CharField(max_length=100, null=True, blank=True)
    purpose = models.TextField()
    no_of_seats = models.IntegerField(null=True, blank=True)
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_category = models.CharField(
        max_length=100, choices=ROOM_CATEGORY, null=True, blank=True
    )
    no_of_participants = models.IntegerField(null=True, blank=True)
    wifi = models.BooleanField(default=False)
    photocopy = models.BooleanField(default=False)
    printing = models.BooleanField(default=False)
    interactive_board = models.BooleanField(default=False)
    whiteboard_marker = models.BooleanField(default=False)
    tea_coffee_water = models.BooleanField(default=False)
    other_service = models.TextField(null=True, blank=True)

    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.booking_date}"


class RescheduleRequest(models.Model):
    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    )

    booking = models.ForeignKey(
        IncubationCenter,
        on_delete=models.CASCADE,
        related_name="reschedule_requests",
        null=True,
        blank=True,
    )
    new_booking_date = models.DateField(null=True, blank=True)
    new_start_time = models.TimeField(null=True, blank=True)
    new_end_time = models.TimeField(null=True, blank=True)
    new_room_category = models.CharField(
        max_length=100, choices=IncubationCenter.ROOM_CATEGORY, null=True, blank=True
    )
    new_booking_type = models.CharField(
        max_length=100, choices=IncubationCenter.BOOKING_CHOICE, null=True, blank=True
    )

    reason = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reschedule Request for {self.booking.name} - {self.status}"
