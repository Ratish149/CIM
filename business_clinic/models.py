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

class NatureOfIndustrySubSubCategory(models.Model):
    sub_category=models.ForeignKey(NatureOfIndustrySubCategory, on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Business_Clinic(models.Model):
    INDUSTRY_CHOICES=(
        ('Startup','Startup'),
        ('Micro','Micro'),
        ('Cottage','Cottage'),
        ('Small','Small'),
        ('Medium','Medium'),
        ('Large','Large'),
    )
    issue=models.TextField()
    issue_image=models.ImageField(upload_to='images/',null=True,blank=True)
    
    issue_sub_category=models.ForeignKey(IssueSubCategory, on_delete=models.CASCADE)
    
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

    nature_of_industry_sub_sub_category=models.ForeignKey(NatureOfIndustrySubSubCategory, on_delete=models.CASCADE)

    member_of_CIM=models.BooleanField(default=False)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name_of_company
