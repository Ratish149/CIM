from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
   DESIGNATION_CHOICES = [
      ('CEO', 'Chief Executive Officer'),
      ('CFO', 'Chief Financial Officer'),
      ('CTO', 'Chief Technology Officer'),
      ('CMO', 'Chief Marketing Officer'),
      ('COO', 'Chief Operating Officer'),
      ('CIO', 'Chief Information Officer'),
      ('CSO', 'Chief Security Officer'),
      ('Other', 'Other'),
   ]

   bio = models.TextField(blank=True)
   date_of_birth = models.DateField(null=True, blank=True)
   phone_number = models.CharField(max_length=15, blank=True)
   address = models.TextField(blank=True)
   designation = models.CharField(max_length=100, choices=DESIGNATION_CHOICES,default='Other')
   alternate_no = models.CharField(max_length=20, blank=True, null=True)

   def __str__(self):
      return self.email

class Organization(models.Model):
   user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='organizations')
   name = models.CharField(max_length=255)
   email = models.EmailField(unique=True)
   phone_number = models.CharField(max_length=15, blank=True)
   address = models.TextField(blank=True)
   website = models.URLField(blank=True)
   country = models.CharField(max_length=100, default='Nepal')
   province_state = models.CharField(max_length=100, default='Province 1')
   municipality_ward = models.CharField(max_length=100, default='Biratnagar')
   logo = models.FileField(upload_to='organization_logos/', blank=True)


   def __str__(self):
      return self.name
   

class File(models.Model):
   organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='files',blank=True,null=True)
   file = models.FileField(upload_to='organization_files/')
   name = models.CharField(max_length=255)
   uploaded_at = models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return self.name
