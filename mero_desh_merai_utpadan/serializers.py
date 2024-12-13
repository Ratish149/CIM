from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings
from .models import NatureOfIndustryCategory, NatureOfIndustrySubCategory, MeroDeshMeraiUtpadan

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
        self.send_confirmation_email(mero_desh_merai_utpadan_instance)
        return mero_desh_merai_utpadan_instance
    
    def send_confirmation_email(self, business_clinic_instance):
        # Email content
        subject = 'Thank You for Participating in the "Mero Desh Merai Utpadan" Campaign'
        message = f"""
Dear Nepali Producers,

Namaste.

We extend our heartfelt gratitude for your participation in the "Mero Desh Merai Utpadan" campaign. Your support is invaluable in our collective effort to promote Nepali products and industries.

We are pleased to inform you that you can now use the mnemonic logo on your desired products and placements. The logo has been sent to your email for your convenience.

Together, we will enhance the visibility and reputation of Nepali products, fostering a stronger economy and a vibrant industrial ecosystem.
Thank you very much for your continued support and commitment.

Warm regards,
Chamber of Industries Morang (CIM)
        """

        recipient_list = [business_clinic_instance.contact_email]  # Assuming the model has an 'email' field

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False,
        )
