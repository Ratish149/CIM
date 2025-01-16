from rest_framework import serializers
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from .models import NatureOfIndustryCategory, NatureOfIndustrySubCategory, MeroDeshMeraiUtpadan,ContactForm
from django.template.loader import render_to_string
import os


class NatureOfIndustryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NatureOfIndustryCategory
        fields = '__all__'  # or specify fields as needed

class NatureOfIndustrySubCategorySerializer(serializers.ModelSerializer):
    category = NatureOfIndustryCategorySerializer(read_only=True)
    class Meta:
        model = NatureOfIndustrySubCategory
        fields = '__all__'  # or specify fields as needed


class MeroDeshMeraiUtpadanSerializer(serializers.ModelSerializer):
    nature_of_industry_category=serializers.PrimaryKeyRelatedField(queryset=NatureOfIndustryCategory.objects.all())
    
    nature_of_industry_sub_category = serializers.PrimaryKeyRelatedField(queryset=NatureOfIndustrySubCategory.objects.all())
    nature_of_industry_sub_category_detail = NatureOfIndustrySubCategorySerializer(source='nature_of_industry_sub_category',read_only=True)
    class Meta:
        model = MeroDeshMeraiUtpadan
        fields = '__all__'  # or specify fields as needed

    def create(self, validated_data):
        mero_desh_merai_utpadan_instance = MeroDeshMeraiUtpadan.objects.create(**validated_data)
        mero_desh_merai_utpadan_instance.save()
        if mero_desh_merai_utpadan_instance.contact_email:
            self.send_confirmation_email(mero_desh_merai_utpadan_instance)
        return mero_desh_merai_utpadan_instance
    
    def send_confirmation_email(self, mero_desh_merai_utpadan_instance):
        subject = 'Thank You for Participating in the "Mero Desh Merai Utpadan" Campaign'
        
        # Generate the file system path for the logo
        logo_path = os.path.join(settings.STATIC_ROOT, 'logo', 'mdmu-logo.png')
        print(f"Logo file system path: {logo_path}")  # Debugging line

        # Load the HTML template
        message = render_to_string('email_template/mdmu_email_template.html', {
            'issue': mero_desh_merai_utpadan_instance,
            'logo_url': logo_path,
        })

        recipient_list = [mero_desh_merai_utpadan_instance.contact_email]  # Assuming the model has an 'email' field

        # Create an EmailMessage instance
        email = EmailMessage(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
        )
        
        # Attach the logo
        with open(logo_path, 'rb') as logo_file:
            email.attach('mdmu-logo.png', logo_file.read(), 'image/png')  # Attach the logo

        email.content_subtype = 'html'  # Set the content type to HTML

        email.send(fail_silently=False)  # Send the email

class ContactFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactForm
        fields = '__all__'

