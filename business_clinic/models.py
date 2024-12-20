from django.db import models

# Create your models here.

class IssueCategory(models.Model):
    name=models.CharField(max_length=255)
    def __str__(self):
        return self.name
    
class IssueSubCategory(models.Model):
    category=models.ForeignKey(IssueCategory, on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    def __str__(self):
        return self.name

class NatureOfIndustryCategory(models.Model):
    name=models.CharField(max_length=255)
    def __str__(self):
        return self.name

class NatureOfIndustrySubCategory(models.Model):
    category=models.ForeignKey(NatureOfIndustryCategory, on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    def __str__(self):
        return self.name


class Issue(models.Model):
    INDUSTRY_CHOICES=(
        ('Startup','Startup'),
        ('Micro','Micro'),
        ('Cottage','Cottage'),
        ('Small','Small'),
        ('Medium','Medium'),
        ('Large','Large'),
    )
    PROGRESS_STATUS=(
        ('Issue Registere and documented','Issue Registere and documented'),
        ('Issue under desk study','Issue under desk study'),
        ('Issue forwarded to concern department','Issue forwarded to concern department'),
        ('Issue solve','Issue solve'),
        ('Issue rejected','Issue rejected'),
    )
    
    issue=models.TextField()
    issue_image=models.ImageField(upload_to='images/',null=True,blank=True)
    
    issue_category=models.ForeignKey(IssueCategory, on_delete=models.CASCADE,null=True,blank=True)
    issue_sub_category=models.ForeignKey(IssueSubCategory, on_delete=models.CASCADE,null=True,blank=True)
    
    is_industry_specific=models.BooleanField(default=False,null=True,blank=True)
    is_common_issue=models.BooleanField(default=False,null=True,blank=True)
    is_specific_policy_related=models.BooleanField(default=False,null=True,blank=True)
    is_procedural_hurdle=models.BooleanField(default=False,null=True,blank=True)
    is_implementation_level=models.BooleanField(default=False,null=True,blank=True)
    is_policy_level=models.BooleanField(default=False,null=True,blank=True)
    is_capacity_scaleup_needed=models.BooleanField(default=False,null=True,blank=True)
    
    progress_status=models.CharField(max_length=255,choices=PROGRESS_STATUS,null=True,blank=True)
    name_of_company=models.CharField(max_length=255)
    address_province=models.CharField(max_length=255)
    address_district=models.CharField(max_length=255)
    address_municipality=models.CharField(max_length=255)
    address_ward=models.CharField(max_length=255)
    address_street=models.CharField(max_length=255)
    contact_name=models.CharField(max_length=255)
    contact_number=models.CharField(max_length=255)
    contact_designation=models.CharField(max_length=255)    
    contact_alternate_number=models.CharField(max_length=255,null=True,blank=True)
    contact_email=models.EmailField(null=True,blank=True)

    nature_of_industry_category=models.ForeignKey(NatureOfIndustryCategory, on_delete=models.CASCADE)
    nature_of_industry_sub_category=models.ForeignKey(NatureOfIndustrySubCategory, on_delete=models.CASCADE)

    member_of_CIM=models.BooleanField(default=False,null=True,blank=True)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name_of_company
