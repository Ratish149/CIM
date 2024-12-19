from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings
from .models import IssueCategory,IssueSubCategory,NatureOfIndustryCategory,NatureOfIndustrySubCategory,Issue

class IssueCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueCategory
        fields = '__all__'

class IssueSubCategorySerializer(serializers.ModelSerializer):
    category=IssueCategorySerializer(read_only=True)
    class Meta:
        model = IssueSubCategory
        fields = '__all__'

class NatureOfIndustryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NatureOfIndustryCategory
        fields = '__all__'

class NatureOfIndustrySubCategorySerializer(serializers.ModelSerializer):
    category=NatureOfIndustryCategorySerializer(read_only=True)
    class Meta:
        model = NatureOfIndustrySubCategory
        fields = '__all__'

class IssueSerializer(serializers.ModelSerializer):
    issue_category=serializers.PrimaryKeyRelatedField(queryset=IssueCategory.objects.all(),required=False)
    
    issue_sub_category = serializers.PrimaryKeyRelatedField(queryset=IssueSubCategory.objects.all(),required=False)  # For input
    issue_sub_category_detail = IssueSubCategorySerializer(source='issue_sub_category', read_only=True)  # For output
    
    nature_of_industry_category = serializers.PrimaryKeyRelatedField(queryset=NatureOfIndustryCategory.objects.all(), required=True)  # Assuming this is still required
    nature_of_industry_sub_category = serializers.PrimaryKeyRelatedField(queryset=NatureOfIndustrySubCategory.objects.all(), required=False)  # Set required=False
    nature_of_industry_sub_category_detail = NatureOfIndustrySubCategorySerializer(source='nature_of_industry_sub_category', read_only=True)  # For output# For output
    class Meta:
        model = Issue
        fields = '__all__'

    def create(self, validated_data):
        # Create the Business_Clinic instance
        issue = Issue.objects.create(**validated_data)
        print(issue)

        issue.save()
        # Send confirmation email
        self.send_confirmation_email(issue)

        return issue

    def send_confirmation_email(self, issue):
        # Email content
        subject = 'Thank You for Registering Your Issues at CIM Business Clinic'
        message = f"""
Dear Industrialists,

Namaste.

Thank you for registering your issues at the CIM Business Clinic. The CIM Business Clinic is a systematic policy advocacy framework of the Chamber of Industries Morang (CIM).

We take your concerns seriously and will conduct thorough research to address them. Your issues will be forwarded to the relevant departments for necessary action. We will keep you updated on the progress.

The information you have provided serves as vital input for CIM's policy advocacy campaign. Together, we can create a better economic environment.
Thank you for your continued support and collaboration.

Warm regards,
Chamber of Industries Morang (CIM)
        """

        recipient_list = [issue.contact_email]  # Assuming the model has an 'email' field

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False,
        )