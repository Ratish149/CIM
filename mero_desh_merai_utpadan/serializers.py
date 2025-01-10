from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings
from .models import NatureOfIndustryCategory, NatureOfIndustrySubCategory, MeroDeshMeraiUtpadan
from django.template.loader import render_to_string
from django.templatetags.static import static


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
        
            # Generate URLs for the logo
        logo_url = static('logo/mdmu-logo.png')  # Use Django's static function
        logo_download_url = 'https://cim.baliyoventures.com' + logo_url  # Update this with your domain
        print(logo_url)
        print(logo_download_url)

        # Load the HTML template
        message = render_to_string('email_template/mdmu_email_template.html', {
            'issue': mero_desh_merai_utpadan_instance,
            'logo_url': logo_url,
            'logo_download_url': logo_download_url,
        })
        # Load the HTML template
        message = render_to_string('email_template/mdmu_email_template.html', {'issue': mero_desh_merai_utpadan_instance})

        recipient_list = [mero_desh_merai_utpadan_instance.contact_email]  # Assuming the model has an 'email' field

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False,
            html_message=message  # Send as HTML
        )
