from rest_framework import serializers
from django.core.mail import send_mail,EmailMessage
from django.conf import settings
from .models import NatureOfIndustryCategory, NatureOfIndustrySubCategory, Issue, IssueAction
from django.template.loader import render_to_string

class NatureOfIndustryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NatureOfIndustryCategory
        fields = ['id', 'name']

class NatureOfIndustrySubCategorySerializer(serializers.ModelSerializer):
    category = NatureOfIndustryCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=NatureOfIndustryCategory.objects.all(),
        source='category',
        write_only=True
    )

    class Meta:
        model = NatureOfIndustrySubCategory
        fields = ['id', 'name', 'category', 'category_id']

class IssueActionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = IssueAction
        fields = [
            'id', 
            'issue', 
            'action_type', 
            'old_status', 
            'new_status',
            'old_value',
            'new_value',
            'comment',
            'created_at',
        ]
        read_only_fields = ('created_at',)

class IssueSerializer(serializers.ModelSerializer):
    nature_of_industry_category = serializers.PrimaryKeyRelatedField(
        queryset=NatureOfIndustryCategory.objects.all(),
        required=False,
        allow_null=True
    )
    nature_of_industry_sub_category = serializers.PrimaryKeyRelatedField(
        queryset=NatureOfIndustrySubCategory.objects.all(),
        required=False,
        allow_null=True
    )
    nature_of_industry_category_detail = NatureOfIndustryCategorySerializer(
        source='nature_of_industry_category',
        read_only=True
    )
    nature_of_industry_sub_category_detail = NatureOfIndustrySubCategorySerializer(
        source='nature_of_industry_sub_category',
        read_only=True
    )
    actions = IssueActionSerializer(many=True, read_only=True)

    class Meta:
        model = Issue
        fields = '__all__'

    def create(self, validated_data):
        issue = Issue.objects.create(**validated_data)
        
        if issue.contact_email:
            self.send_confirmation_email(issue)
        
        return issue

    def send_confirmation_email(self, issue):
        subject = 'Thank You for Registering Your Issues at CIM Business Clinic'
        
        # Load the HTML template
        message = render_to_string('email_template/email_template.html', {'issue': issue})

        email = EmailMessage(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [issue.contact_email],
        reply_to=["biratexpo2024@gmail.com"],
    )
    
        # Set content type to HTML
        email.content_subtype = "html"  # This ensures the email is rendered as HTML
        email.send()