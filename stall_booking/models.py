from django.db import models
from django.core.mail import send_mail
from django.conf import settings

class StallBooking(models.Model):

    STALL_TYPE_CHOICES = [
         ('National Prime', 'National Prime'),
         ('National General', 'National General'),
         ('International', 'International'),
         ('Agro and MSME', 'Agro and MSME'),
         ('Automobiles', 'Automobiles'),
         ('Food Stalls', 'Food Stalls'),
         ('BDS Providers Stall', 'BDS Providers Stall'),
    ]

    MERGE_CHOICES = [
        ('Merge', 'Merge'),
        ('Separate', 'Separate'),
    ]

    STATUS = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    # Organization/Company Information
    company = models.CharField(max_length=255)
    address = models.TextField()
    chief_executive = models.CharField(max_length=255)
    phone = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    email = models.EmailField()
    status = models.CharField(max_length=100, choices=STATUS, default='Pending')

    # Stall Information
    stall_type = models.CharField(max_length=200, choices=STALL_TYPE_CHOICES)
    stall_no = models.CharField(max_length=200)
    merge_or_separate = models.CharField(max_length=100, choices=MERGE_CHOICES)

    # Payment Information
    voucher = models.FileField(upload_to='vouchers/')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    advance_amount = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_in_words = models.TextField()

    # Terms and Conditions
    terms_and_conditions_accepted = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company} - Stall {self.stall_no}"
    
    def has_paid_all(self):
        return self.remaining_amount == 0

    class Meta:
        verbose_name = "Stall Booking"
        verbose_name_plural = "Stall Bookings"


class SponsorBooking(models.Model):
    STALL_TYPE_CHOICES = [
        ('Main Sponsor', 'Main Sponsor'),
        ('Powered By Sponsor', 'Powered By Sponsor'),
        ('Platinum', 'Platinum'),
        ('Diamond', 'Diamond'),
        ('Gold', 'Gold'),
        ('Partner Sponsor', 'Partner Sponsor'),
        ('Silver', 'Silver'),
    ]

    stall_type = models.CharField(max_length=200, choices=STALL_TYPE_CHOICES)
    stall_id = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200,blank=True, null=True)
    company_email = models.CharField(max_length=200,blank=True, null=True)
    contact_number = models.CharField(max_length=200,blank=True, null=True)

    def __str__(self):
        return f"{self.company_name} - {self.stall_id}"

# Model for Thematic Session
class ThematicSession(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    start_time = models.TimeField()
    end_time=models.TimeField(blank=True, null=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
    
class SubSession(models.Model):
    thematic_session = models.ForeignKey(
        ThematicSession, 
        on_delete=models.CASCADE, 
        related_name="sub_sessions"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.thematic_session.title}"


class Panelist(models.Model):
    ROLE_CHOICES = [
        ('Theme Chair', 'Theme Chair'),
        ('Chief Guest', 'Chief Guest'),
        ('Guest of Honor', 'Guest of Honor'),
        ('Moderator', 'Moderator'),
        ('Keynote Speaker', 'Keynote Speaker'),
        ('Speaker', 'Speaker'),
        ('Guest', 'Guest'),
        ('Discussion Leader', 'Discussion Leader'),
        ('Presenter', 'Presenter'),
    ]
    thematic_session=models.ManyToManyField(ThematicSession, related_name="thematicpanelists",blank=True)
    sub_session = models.ManyToManyField(
        SubSession, 
        
        related_name="panelists",
        blank=True
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    name = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to="panelists/", blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    biodata = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.role}: {self.name}"

# Model for Thematic Registration
class ThematicRegistration(models.Model):
    PARTICIPANT_TYPE_CHOICES = [
        ('Speaker', 'Speaker'),
        ('Participant', 'Participant'),
    ]
    FOOD_CHOICES = [
        ('Veg', 'Veg'),
        ('Non Veg', 'Non Veg'),
    ]
    HOTEL_ACCOMODATION_CHOICES = [
        ('Self', 'Self'),
        ('CIM', 'CIM'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    name = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    contact = models.CharField(max_length=15)
    participant= models.CharField(max_length=20, choices=PARTICIPANT_TYPE_CHOICES)

    arrival_date = models.DateField(null=True, blank=True)
    departure_date = models.DateField(null=True, blank=True)
    flight_no = models.CharField(max_length=20, null=True, blank=True)
    flight_time = models.TimeField(null=True, blank=True)
    return_flight_no = models.CharField(max_length=20, null=True, blank=True)
    return_flight_time = models.TimeField(null=True, blank=True)
    airline= models.CharField(max_length=50,null=True, blank=True)
    
    food= models.CharField(max_length=20, choices=FOOD_CHOICES,null=True, blank=True)
    hotel_accomodation= models.CharField(max_length=20, choices=HOTEL_ACCOMODATION_CHOICES,null=True, blank=True)
    check_in_date = models.DateField(null=True, blank=True)
    check_out_date = models.DateField(null=True, blank=True)
    hotel= models.CharField(max_length=220,null=True, blank=True)

    sessions = models.ManyToManyField(ThematicSession, related_name='registrations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.name} - {self.organization}"

class GuidedTour(models.Model):
    # College Details
    college_name = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    municipality = models.CharField(max_length=255)
    ward = models.CharField(max_length=50)
   
    # Contact Details
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    contact_person_name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    mobile_no = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )    
    # Tour Details
    tour_date = models.DateField()
    number_of_students = models.PositiveIntegerField()
    STUDENT_LEVEL_CHOICES = [
        ('10+2', '10+2'),
        ('Bachelors', 'Bachelors'),
        ('Masters', 'Masters'),
        ('Mixed', 'Mixed'),
    ]
    student_level = models.CharField(
        max_length=20,
        choices=STUDENT_LEVEL_CHOICES,
        default='10+2'
    )

    def __str__(self):
        return f"{self.college_name} - {self.tour_date}"



class Invitation(models.Model):
    STATUS_CHOICES = [
        ('ACCEPTED', 'ACCEPTED'),
        ('REJECTED', 'REJECTED'),
    ]
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15,blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACCEPTED')
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.company_name}"