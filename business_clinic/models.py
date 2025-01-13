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

    IMPLEMENTATION_LEVEL_CHOICES = [
        ('Policy Level', 'Policy Level'),
        ('Implementation Level', 'Implementation Level'),
        ('Capacity Scale Up', 'Capacity Scale Up'),
    ]

    # Issue Details
    title = models.CharField(max_length=255, help_text="Brief title of the issue",default='')
    description = models.TextField(verbose_name="Issue Description",default='')
    issue_image = models.FileField(null=True, blank=True, upload_to='issue_images/')
    
    # Categorization
    nature_of_issue = models.CharField(max_length=255,choices=NATURE_OF_ISSUE_CHOICES,default='Other',null=True,blank=True)
    industry_specific_or_common_issue = models.BooleanField(default=False)
    policy_related_or_procedural_issue = models.BooleanField(default=False)
    
    # Industry Information
    industry_size = models.CharField(max_length=20, choices=INDUSTRY_SIZE_CHOICES,default='Other',null=True,blank=True)
    nature_of_industry_category = models.ForeignKey(NatureOfIndustryCategory, on_delete=models.CASCADE,default=None,null=True,blank=True)
    nature_of_industry_sub_category = models.ForeignKey(NatureOfIndustrySubCategory, on_delete=models.CASCADE,default=None,null=True,blank=True)
    
    # Company Information
    name_of_company = models.CharField(max_length=255,default='',null=True,blank=True)
    member_of_CIM = models.BooleanField(default=False)
    
    # Address Information
    address_province = models.CharField(max_length=255,default='',null=True,blank=True)
    address_district = models.CharField(max_length=255,default='',null=True,blank=True)
    address_municipality = models.CharField(max_length=255,default='',null=True,blank=True)
    address_ward = models.CharField(max_length=255,default='',null=True,blank=True)
    address_street = models.CharField(max_length=255,default='',null=True,blank=True)
    
    # Contact Information
    contact_name = models.CharField(max_length=255,default='',null=True,blank=True)
    contact_designation = models.CharField(max_length=255,default='',null=True,blank=True)
    contact_number = models.CharField(max_length=255,default='',null=True,blank=True)
    contact_alternate_number = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    
    # Status and Tracking
    progress_status = models.CharField(
        max_length=50,
        choices=PROGRESS_STATUS_CHOICES,
        default='Issue Registered and Documented',
        null=True,blank=True
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Update the implementation level field to use choices
    implementation_level = models.CharField(
        max_length=50,
        choices=IMPLEMENTATION_LEVEL_CHOICES,
        default='Implementation Level',
        null=True,blank=True
    )

    # Add new boolean fields
    share_contact_details = models.BooleanField(
        default=False,
        help_text="Allow sharing contact details with concerned authorities"
    )
    forward_to_authority = models.BooleanField(
        default=False,
        help_text="Forward this issue to concerned authority"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Issue"
        verbose_name_plural = "Issues"

    def __str__(self):
        return f"{self.title} - {self.name_of_company}"

    def save(self, *args, **kwargs):
        # Get the current state from the database if this is an existing object
        if self.pk:
            old_instance = Issue.objects.get(pk=self.pk)
            
            # Check for status change
            if old_instance.progress_status != self.progress_status:
                IssueAction.objects.create(
                    issue=self,
                    action_type='status_change',
                    old_status=old_instance.progress_status,
                    new_status=self.progress_status
                )

            # Check for implementation level change
            if old_instance.implementation_level != self.implementation_level:
                IssueAction.objects.create(
                    issue=self,
                    action_type='implementation_level_change',
                    old_value=old_instance.implementation_level,
                    new_value=self.implementation_level
                )

            # Check for share contact details change
            if old_instance.share_contact_details != self.share_contact_details:
                IssueAction.objects.create(
                    issue=self,
                    action_type='share_contact_change',
                    old_value=str(old_instance.share_contact_details),
                    new_value=str(self.share_contact_details)
                )

            # Check for forward to authority change
            if old_instance.forward_to_authority != self.forward_to_authority:
                IssueAction.objects.create(
                    issue=self,
                    action_type='forward_authority_change',
                    old_value=str(old_instance.forward_to_authority),
                    new_value=str(self.forward_to_authority)
                )

            # Check for nature of industry category change
            if old_instance.nature_of_industry_category != self.nature_of_industry_category:
                IssueAction.objects.create(
                    issue=self,
                    action_type='industry_category_change',
                    old_value=str(old_instance.nature_of_industry_category),
                    new_value=str(self.nature_of_industry_category)
                )

            # Check for nature of industry subcategory change
            if old_instance.nature_of_industry_sub_category != self.nature_of_industry_sub_category:
                IssueAction.objects.create(
                    issue=self,
                    action_type='industry_subcategory_change',
                    old_value=str(old_instance.nature_of_industry_sub_category),
                    new_value=str(self.nature_of_industry_sub_category)
                )

            # Check for nature of issue change
            if old_instance.nature_of_issue != self.nature_of_issue:
                IssueAction.objects.create(
                    issue=self,
                    action_type='nature_of_issue_change',
                    old_value=old_instance.nature_of_issue,
                    new_value=self.nature_of_issue
                )

        super().save(*args, **kwargs)

# Add this new model to track issue actions
class IssueAction(models.Model):
    issue = models.ForeignKey('Issue', on_delete=models.CASCADE, related_name='actions')
    action_type = models.CharField(max_length=50, choices=[
        ('status_change', 'Status Change'),
        ('comment', 'Comment'),
        ('assignment', 'Assignment'),
        ('forward_to_authority', 'Forward to Authority'),
        ('implementation_level_change', 'Implementation Level Change'),
        ('share_contact_change', 'Share Contact Change'),
        ('forward_authority_change', 'Forward Authority Change'),
        ('industry_category_change', 'Industry Category Change'),
        ('industry_subcategory_change', 'Industry Subcategory Change'),
        ('nature_of_issue_change', 'Nature of Issue Change'),
    ])
    old_status = models.CharField(max_length=50, blank=True, null=True)
    new_status = models.CharField(max_length=50, blank=True, null=True)
    old_value = models.CharField(max_length=255, blank=True, null=True)  # For storing old values of any field
    new_value = models.CharField(max_length=255, blank=True, null=True)  # For storing new values of any field
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.action_type} on {self.issue.title} at {self.created_at}"
 