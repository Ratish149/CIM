from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import qrcode
from io import BytesIO
from django.core.files import File
import json
from django.core.files.base import ContentFile
from django.db.models import Count

class Topic(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    venue = models.CharField(max_length=200)
    image=models.FileField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    time_slots = models.JSONField(default=list)

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("End date cannot be before start date")

    def __str__(self):
        return self.name
    
    def create_time_slots(self):
    # Clear existing time slots for this topic
        TimeSlot.objects.filter(topic=self).delete()
        
        # Define the time slots for each day
        time_slots = self.time_slots  # Assuming this is a list of dicts from the JSON field
        
        current_date = self.start_date
        while current_date <= self.end_date:
            for slot in time_slots:
                TimeSlot.objects.create(
                    topic=self,
                    date=current_date,
                    start_time=slot['start_time'],
                    end_time=slot['end_time'],
                    max_participants=20,  # Set default or modify as needed
                    current_participants=0  # Set default or modify as needed
                )
            current_date += timezone.timedelta(days=1)  # Move to the next day
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the Topic instance first
        self.create_time_slots()  # Create time slots after saving the Topic


class TimeSlot(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='time_slot_instances')
    date = models.DateField(default=timezone.now)
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(default=timezone.now)
    max_participants = models.IntegerField(default=0)
    current_participants = models.IntegerField(default=0)

    def is_available(self):
        return self.current_participants < self.max_participants
    
    def available_spots(self):
        return self.max_participants - self.current_participants

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time")
        if self.max_participants < 1:
            raise ValidationError("Maximum participants must be at least 1")

    def __str__(self):
        return f"{self.topic.name}: {self.date.strftime('%Y-%m-%d')} {self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')}"


class Registration(models.Model):
    REGISTRATION_TYPES = [
        ('Single Person', 'Single Person'),
        ('Group', 'Group'),
        ('Expo Access', 'Expo Access')
    ]
    PAYMENT_METHODS = [
        ('Nabil Bank', 'Nabil Bank'),
    ]
    REGISTRATION_STATUS = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled')
    ]

    PRICE_CONFIG = {
        'Single Person': 300,
        'Group': 1500,
        'Expo Access': 2100
    }

    # Basic Fields
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    registration_type = models.CharField(max_length=20, choices=REGISTRATION_TYPES)
    status = models.CharField(max_length=20, choices=REGISTRATION_STATUS, default='Pending')
    
    # Participant Info
    first_name = models.CharField(max_length=220, blank=True, null=True)
    last_name = models.CharField(max_length=220, blank=True, null=True)
    email = models.EmailField()
    group_members=models.JSONField(blank=True, null=True)

    qualification = models.CharField(max_length=20, choices=[
        ('Under SEE', 'Under SEE'),
        ('10+2', '10+2'),
        ('Graduate', 'Graduate'),
        ('Post Graduate', 'Post Graduate'),
    ])
    gender = models.CharField(max_length=10, choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ])
    age = models.IntegerField(validators=[MinValueValidator(10)])
    address = models.TextField()
    mobile_number = models.CharField(
        max_length=20, 
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'"
        )]
    )
    
    
    # Payment and Status
    total_participants = models.IntegerField(validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_screenshot = models.ImageField(blank=True, null=True)
    
    # Flags
    agreed_to_no_refund = models.BooleanField(default=False)
    is_early_bird = models.BooleanField(default=False)
    is_expo_access = models.BooleanField(default=False)
    is_free_entry = models.BooleanField(default=False)
    
    # QR Code
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)
    is_attended = models.BooleanField(default=False,null=True,blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def generate_qr_code(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        # Directly add the link to the QR code
        link = f"https://biratexpo.cim.org.np/live-training/participants/{self.id}"
        qr.add_data(link)  # Changed to add only the link
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        blob = BytesIO()
        img.save(blob, 'PNG')
        
        self.qr_code.save(
            f'qr_code_{self.id}.png',
            ContentFile(blob.getvalue()),
            save=False
        )

    def save(self, *args, **kwargs):
        # Check if this is a new registration
        is_new = self._state.adding
        
        # Check early bird eligibility
        early_bird_date = timezone.datetime(2025, 1, 18).date()
        self.is_early_bird = timezone.now().date() <= early_bird_date

        # Calculate total price
        if self.registration_type == 'Single Person':
            self.total_price = self.PRICE_CONFIG['Single Person'] * self.total_participants
        elif self.registration_type == 'Group':
            self.total_price = self.PRICE_CONFIG['Group']
        elif self.registration_type == 'Expo Access':
            self.total_price = self.PRICE_CONFIG['Expo Access']

        # Save first to get the ID
        super().save(*args, **kwargs)

        # Handle post-save actions for new confirmed registrations
        if is_new or (not is_new and self.status == 'Confirmed'):
            try:
                # Generate QR code if needed
                if not self.qr_code:
                    self.generate_qr_code()
                    super().save(update_fields=['qr_code'])
                
                # Send confirmation email
                # self.send_confirmation_email()
            except Exception as e:
                print(f"Error in post-save processing: {str(e)}")

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.time_slot.topic.name} ({self.created_at.strftime('%Y-%m-%d %H:%M:%S')})"