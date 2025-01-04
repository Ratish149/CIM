from django.db import models

class NatureOfIndustryCategory(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Nature of Industry Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class NatureOfIndustrySubCategory(models.Model):
    category = models.ForeignKey(NatureOfIndustryCategory, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Nature of Industry Sub Categories"
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class Issue(models.Model):
    INDUSTRY_SIZE_CHOICES = [
        ('Startup', 'Startup'),
        ('Micro', 'Micro'),
        ('Cottage', 'Cottage'),
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
    ]
    
    PROGRESS_STATUS_CHOICES = [
        ('Issue Registered and Documented', 'Issue Registered and Documented'),
        ('Issue Under Desk Study', 'Issue Under Desk Study'),
        ('Issue Forwarded to Concerned Department', 'Issue Forwarded to Concerned Department'),
        ('Issue Solved', 'Issue Solved'),
        ('Issue Rejected', 'Issue Rejected'),
    ]

    NATURE_OF_ISSUE_CHOICES = [
        ('Energy', 'Energy'),
        ('Human Resources – Labour', 'Human Resources – Labour'),
        ('Tax & Revenue', 'Tax & Revenue'),
        ('Bank & Finance', 'Bank & Finance'),
        ('Export', 'Export'),
        ('Import Substitution & Domestic Product Promotion', 'Import Substitution & Domestic Product Promotion'),
        ('Transport & Transit', 'Transport & Transit'),
        ('Local Government', 'Local Government'),
        ('Provincial Government', 'Provincial Government'),
        ('Other', 'Other'),
    ]

    # Issue Details
    title = models.CharField(max_length=255, help_text="Brief title of the issue",default='')
    description = models.TextField(verbose_name="Issue Description",default='')
    issue_image = models.FileField( null=True, blank=True)
    
    # Categorization
    nature_of_issue = models.CharField(max_length=255,choices=NATURE_OF_ISSUE_CHOICES,default='Other')
    industry_specific_or_common_issue = models.BooleanField(default=False)
    policy_related_or_procedural_issue = models.BooleanField(default=False)
    implementation_level_policy_level_or_capacity_scale = models.BooleanField(default=False)
    
    # Industry Information
    industry_size = models.CharField(max_length=20, choices=INDUSTRY_SIZE_CHOICES,default='Other')
    nature_of_industry_category = models.ForeignKey(NatureOfIndustryCategory, on_delete=models.CASCADE,default=None)
    nature_of_industry_sub_category = models.ForeignKey(NatureOfIndustrySubCategory, on_delete=models.CASCADE,default=None)
    
    # Company Information
    name_of_company = models.CharField(max_length=255,default='')
    member_of_CIM = models.BooleanField(default=False)
    
    # Address Information
    address_province = models.CharField(max_length=255,default='')
    address_district = models.CharField(max_length=255,default='')
    address_municipality = models.CharField(max_length=255,default='')
    address_ward = models.CharField(max_length=255,default='')
    address_street = models.CharField(max_length=255,default='')
    
    # Contact Information
    contact_name = models.CharField(max_length=255,default='')
    contact_designation = models.CharField(max_length=255,default='')
    contact_number = models.CharField(max_length=255,default='')
    contact_alternate_number = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    
    # Status and Tracking
    progress_status = models.CharField(
        max_length=50,
        choices=PROGRESS_STATUS_CHOICES,
        default='Issue Registered and Documented'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Issue"
        verbose_name_plural = "Issues"

    def __str__(self):
        return f"{self.title} - {self.name_of_company}"
