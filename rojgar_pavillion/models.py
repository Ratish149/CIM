from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.utils import timezone

class Topic(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name
    
class TimeSlot(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='time_slots')
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(default=timezone.now)
    max_participants = models.IntegerField(default=0)
    current_participants = models.IntegerField(default=0)

    def is_available(self):
        return self.current_participants < self.max_participants
    
    def available_spots(self):
        return self.max_participants - self.current_participants

    def __str__(self):
        return f"{self.topic.name}: {self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')}"
    
class Registration(models.Model):
    REGISTRATION_TYPES = [
        ('SINGLE', 'Single Person'),
        ('GROUP', 'Group'),
        ('EXPO_ACCESS', 'Expo Access')
    ]
    PAYMENT_METHODS = [
        ('Nabil_Bank', 'Nabil Bank'),
    ]

    PRICE_CONFIG = {
        'SINGLE': 300,
        'GROUP': 1500,
        'EXPO_ACCESS': 2100
    }

    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    registration_type = models.CharField(max_length=20, choices=REGISTRATION_TYPES)
    
    total_participants = models.IntegerField(validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_screenshot = models.ImageField(upload_to='payments/', null=True, blank=True)
    agreed_to_no_refund = models.BooleanField(default=False)
    is_early_bird = models.BooleanField(default=False)
    is_expo_access = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Check early bird eligibility
        early_bird_date = timezone.datetime(2025, 1, 18).date()
        self.is_early_bird = timezone.now().date() <= early_bird_date

        # Calculate total price
        if self.registration_type == 'SINGLE':
            self.total_price = self.PRICE_CONFIG['SINGLE'] * self.total_participants
        elif self.registration_type == 'GROUP':
            self.total_price = self.PRICE_CONFIG['GROUP']
        elif self.registration_type == 'EXPO_ACCESS':
            self.total_price = self.PRICE_CONFIG['EXPO_ACCESS']

        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.time_slot.topic.name} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

class Participant(models.Model):
    QUALIFICATIONS = [
        ('Under SEE', 'Under SEE'),
        ('10+2', '10+2'),
        ('Graduate', 'Graduate'),
        ('Post Graduate', 'Post Graduate'),
    ]
    GENDERS = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    
    mobile_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'"
    )

    registration = models.ForeignKey(
        Registration, 
        on_delete=models.CASCADE, 
        related_name='participants'
    )
    full_name = models.CharField(max_length=200)
    qualification = models.CharField(max_length=20, choices=QUALIFICATIONS)
    gender = models.CharField(max_length=10, choices=GENDERS)
    age = models.IntegerField(validators=[MinValueValidator(14)])
    address = models.TextField()
    mobile_number = models.CharField(max_length=20, validators=[mobile_validator])
    email = models.EmailField()
    is_free_entry = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name